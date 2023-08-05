"""
    pygments.lexers.configs
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for configuration file formats.

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import ExtendedRegexLexer, RegexLexer, default, words, \
    bygroups, include, using
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Whitespace, Literal, Error, Generic
from pygments.lexers.shell import BashLexer
from pygments.lexers.data import JsonLexer

__all__ = ['IniLexer', 'RegeditLexer', 'PropertiesLexer', 'KconfigLexer',
           'Cfengine3Lexer', 'ApacheConfLexer', 'SquidConfLexer',
           'NginxConfLexer', 'LighttpdConfLexer', 'DockerLexer',
           'TerraformLexer', 'TermcapLexer', 'TerminfoLexer',
           'PkgConfigLexer', 'PacmanConfLexer', 'AugeasLexer', 'TOMLLexer',
           'NestedTextLexer', 'SingularityLexer']


class IniLexer(RegexLexer):
    """
    Lexer for configuration files in INI style.
    """

    name = 'INI'
    aliases = ['ini', 'cfg', 'dosini']
    filenames = [
        '*.ini', '*.cfg', '*.inf', '.editorconfig',
        # systemd unit files
        # https://www.freedesktop.org/software/systemd/man/systemd.unit.html
        '*.service', '*.socket', '*.device', '*.mount', '*.automount',
        '*.swap', '*.target', '*.path', '*.timer', '*.slice', '*.scope',
    ]
    mimetypes = ['text/x-ini', 'text/inf']

    tokens = {
        'root': [
            (r'\s+', Whitespace),
            (r'[;#].*', Comment.Single),
            (r'\[.*?\]$', Keyword),
            (r'(.*?)([ \t]*)(=)([ \t]*)([^\t\n]*)',
             bygroups(Name.Attribute, Whitespace, Operator, Whitespace, String)),
            # standalone option, supported by some INI parsers
            (r'(.+?)$', Name.Attribute),
        ],
    }

    def analyse_text(text):
        npos = text.find('\n')
        if npos < 3:
            return False
        return text[0] == '[' and text[npos-1] == ']'


class RegeditLexer(RegexLexer):
    """
    Lexer for `Windows Registry
    <http://en.wikipedia.org/wiki/Windows_Registry#.REG_files>`_ files produced
    by regedit.

    .. versionadded:: 1.6
    """

    name = 'reg'
    aliases = ['registry']
    filenames = ['*.reg']
    mimetypes = ['text/x-windows-registry']

    tokens = {
        'root': [
            (r'Windows Registry Editor.*', Text),
            (r'\s+', Whitespace),
            (r'[;#].*', Comment.Single),
            (r'(\[)(-?)(HKEY_[A-Z_]+)(.*?\])$',
             bygroups(Keyword, Operator, Name.Builtin, Keyword)),
            # String keys, which obey somewhat normal escaping
            (r'("(?:\\"|\\\\|[^"])+")([ \t]*)(=)([ \t]*)',
             bygroups(Name.Attribute, Whitespace, Operator, Whitespace),
             'value'),
            # Bare keys (includes @)
            (r'(.*?)([ \t]*)(=)([ \t]*)',
             bygroups(Name.Attribute, Whitespace, Operator, Whitespace),
             'value'),
        ],
        'value': [
            (r'-', Operator, '#pop'),  # delete value
            (r'(dword|hex(?:\([0-9a-fA-F]\))?)(:)([0-9a-fA-F,]+)',
             bygroups(Name.Variable, Punctuation, Number), '#pop'),
            # As far as I know, .reg files do not support line continuation.
            (r'.+', String, '#pop'),
            default('#pop'),
        ]
    }

    def analyse_text(text):
        return text.startswith('Windows Registry Editor')


class PropertiesLexer(RegexLexer):
    """
    Lexer for configuration files in Java's properties format.

    Note: trailing whitespace counts as part of the value as per spec

    .. versionadded:: 1.4
    """

    name = 'Properties'
    aliases = ['properties', 'jproperties']
    filenames = ['*.properties']
    mimetypes = ['text/x-java-properties']

    tokens = {
        'root': [
            (r'^(\w+)([ \t])(\w+\s*)$', bygroups(Name.Attribute, Whitespace, String)),
            (r'^\w+(\\[ \t]\w*)*$', Name.Attribute),
            (r'(^ *)([#!].*)', bygroups(Whitespace, Comment)),
            # More controversial comments
            (r'(^ *)((?:;|//).*)', bygroups(Whitespace, Comment)),
            (r'(.*?)([ \t]*)([=:])([ \t]*)(.*(?:(?<=\\)\n.*)*)',
             bygroups(Name.Attribute, Whitespace, Operator, Whitespace, String)),
            (r'\s', Whitespace),
        ],
    }


def _rx_indent(level):
    # Kconfig *always* interprets a tab as 8 spaces, so this is the default.
    # Edit this if you are in an environment where KconfigLexer gets expanded
    # input (tabs expanded to spaces) and the expansion tab width is != 8,
    # e.g. in connection with Trac (trac.ini, [mimeviewer], tab_width).
    # Value range here is 2 <= {tab_width} <= 8.
    tab_width = 8
    # Regex matching a given indentation {level}, assuming that indentation is
    # a multiple of {tab_width}. In other cases there might be problems.
    if tab_width == 2:
        space_repeat = '+'
    else:
        space_repeat = '{1,%d}' % (tab_width - 1)
    if level == 1:
        level_repeat = ''
    else:
        level_repeat = '{%s}' % level
    return r'(?:\t| %s\t| {%s})%s.*\n' % (space_repeat, tab_width, level_repeat)


class KconfigLexer(RegexLexer):
    """
    For Linux-style Kconfig files.

    .. versionadded:: 1.6
    """

    name = 'Kconfig'
    aliases = ['kconfig', 'menuconfig', 'linux-config', 'kernel-config']
    # Adjust this if new kconfig file names appear in your environment
    filenames = ['Kconfig*', '*Config.in*', 'external.in*',
                 'standard-modules.in']
    mimetypes = ['text/x-kconfig']
    # No re.MULTILINE, indentation-aware help text needs line-by-line handling
    flags = 0

    def call_indent(level):
        # If indentation >= {level} is detected, enter state 'indent{level}'
        return (_rx_indent(level), String.Doc, 'indent%s' % level)

    def do_indent(level):
        # Print paragraphs of indentation level >= {level} as String.Doc,
        # ignoring blank lines. Then return to 'root' state.
        return [
            (_rx_indent(level), String.Doc),
            (r'\s*\n', Text),
            default('#pop:2')
        ]

    tokens = {
        'root': [
            (r'\s+', Whitespace),
            (r'#.*?\n', Comment.Single),
            (words((
                'mainmenu', 'config', 'menuconfig', 'choice', 'endchoice',
                'comment', 'menu', 'endmenu', 'visible if', 'if', 'endif',
                'source', 'prompt', 'select', 'depends on', 'default',
                'range', 'option'), suffix=r'\b'),
             Keyword),
            (r'(---help---|help)[\t ]*\n', Keyword, 'help'),
            (r'(bool|tristate|string|hex|int|defconfig_list|modules|env)\b',
             Name.Builtin),
            (r'[!=&|]', Operator),
            (r'[()]', Punctuation),
            (r'[0-9]+', Number.Integer),
            (r"'(''|[^'])*'", String.Single),
            (r'"(""|[^"])*"', String.Double),
            (r'\S+', Text),
        ],
        # Help text is indented, multi-line and ends when a lower indentation
        # level is detected.
        'help': [
            # Skip blank lines after help token, if any
            (r'\s*\n', Text),
            # Determine the first help line's indentation level heuristically(!).
            # Attention: this is not perfect, but works for 99% of "normal"
            # indentation schemes up to a max. indentation level of 7.
            call_indent(7),
            call_indent(6),
            call_indent(5),
            call_indent(4),
            call_indent(3),
            call_indent(2),
            call_indent(1),
            default('#pop'),  # for incomplete help sections without text
        ],
        # Handle text for indentation levels 7 to 1
        'indent7': do_indent(7),
        'indent6': do_indent(6),
        'indent5': do_indent(5),
        'indent4': do_indent(4),
        'indent3': do_indent(3),
        'indent2': do_indent(2),
        'indent1': do_indent(1),
    }


class Cfengine3Lexer(RegexLexer):
    """
    Lexer for `CFEngine3 <http://cfengine.org>`_ policy files.

    .. versionadded:: 1.5
    """

    name = 'CFEngine3'
    aliases = ['cfengine3', 'cf3']
    filenames = ['*.cf']
    mimetypes = []

    tokens = {
        'root': [
            (r'#.*?\n', Comment),
            (r'(body)(\s+)(\S+)(\s+)(control)',
             bygroups(Keyword, Whitespace, Keyword, Whitespace, Keyword)),
            (r'(body|bundle)(\s+)(\S+)(\s+)(\w+)(\()',
             bygroups(Keyword, Whitespace, Keyword, Whitespace, Name.Function, Punctuation),
             'arglist'),
            (r'(body|bundle)(\s+)(\S+)(\s+)(\w+)',
             bygroups(Keyword, Whitespace, Keyword, Whitespace, Name.Function)),
            (r'(")([^"]+)(")(\s+)(string|slist|int|real)(\s*)(=>)(\s*)',
             bygroups(Punctuation, Name.Variable, Punctuation,
                      Whitespace, Keyword.Type, Whitespace, Operator, Whitespace)),
            (r'(\S+)(\s*)(=>)(\s*)',
             bygroups(Keyword.Reserved, Whitespace, Operator, Text)),
            (r'"', String, 'string'),
            (r'(\w+)(\()', bygroups(Name.Function, Punctuation)),
            (r'([\w.!&|()]+)(::)', bygroups(Name.Class, Punctuation)),
            (r'(\w+)(:)', bygroups(Keyword.Declaration, Punctuation)),
            (r'@[{(][^)}]+[})]', Name.Variable),
            (r'[(){},;]', Punctuation),
            (r'=>', Operator),
            (r'->', Operator),
            (r'\d+\.\d+', Number.Float),
            (r'\d+', Number.Integer),
            (r'\w+', Name.Function),
            (r'\s+', Whitespace),
        ],
        'string': [
            (r'\$[{(]', String.Interpol, 'interpol'),
            (r'\\.', String.Escape),
            (r'"', String, '#pop'),
            (r'\n', String),
            (r'.', String),
        ],
        'interpol': [
            (r'\$[{(]', String.Interpol, '#push'),
            (r'[})]', String.Interpol, '#pop'),
            (r'[^${()}]+', String.Interpol),
        ],
        'arglist': [
            (r'\)', Punctuation, '#pop'),
            (r',', Punctuation),
            (r'\w+', Name.Variable),
            (r'\s+', Whitespace),
        ],
    }


class ApacheConfLexer(RegexLexer):
    """
    Lexer for configuration files following the Apache config file
    format.

    .. versionadded:: 0.6
    """

    name = 'ApacheConf'
    aliases = ['apacheconf', 'aconf', 'apache']
    filenames = ['.htaccess', 'apache.conf', 'apache2.conf']
    mimetypes = ['text/x-apacheconf']
    flags = re.MULTILINE | re.IGNORECASE

    tokens = {
        'root': [
            (r'\s+', Whitespace),
            (r'#(.*\\\n)+.*$|(#.*?)$', Comment),
            (r'(<[^\s>/][^\s>]*)(?:(\s+)(.*))?(>)',
             bygroups(Name.Tag, Whitespace, String, Name.Tag)),
            (r'(</[^\s>]+)(>)',
             bygroups(Name.Tag, Name.Tag)),
            (r'[a-z]\w*', Name.Builtin, 'value'),
            (r'\.+', Text),
        ],
        'value': [
            (r'\\\n', Text),
            (r'\n+', Whitespace, '#pop'),
            (r'\\', Text),
            (r'[^\S\n]+', Whitespace),
            (r'\d+\.\d+\.\d+\.\d+(?:/\d+)?', Number),
            (r'\d+', Number),
            (r'/([*a-z0-9][*\w./-]+)', String.Other),
            (r'(on|off|none|any|all|double|email|dns|min|minimal|'
             r'os|productonly|full|emerg|alert|crit|error|warn|'
             r'notice|info|debug|registry|script|inetd|standalone|'
             r'user|group)\b', Keyword),
            (r'"([^"\\]*(?:\\(.|\n)[^"\\]*)*)"', String.Double),
            (r'[^\s"\\]+', Text)
        ],
    }


class SquidConfLexer(RegexLexer):
    """
    Lexer for `squid <http://www.squid-cache.org/>`_ configuration files.

    .. versionadded:: 0.9
    """

    name = 'SquidConf'
    aliases = ['squidconf', 'squid.conf', 'squid']
    filenames = ['squid.conf']
    mimetypes = ['text/x-squidconf']
    flags = re.IGNORECASE

    keywords = (
        "access_log", "acl", "always_direct", "announce_host",
        "announce_period", "announce_port", "announce_to", "anonymize_headers",
        "append_domain", "as_whois_server", "auth_param_basic",
        "authenticate_children", "authenticate_program", "authenticate_ttl",
        "broken_posts", "buffered_logs", "cache_access_log", "cache_announce",
        "cache_dir", "cache_dns_program", "cache_effective_group",
        "cache_effective_user", "cache_host", "cache_host_acl",
        "cache_host_domain", "cache_log", "cache_mem", "cache_mem_high",
        "cache_mem_low", "cache_mgr", "cachemgr_passwd", "cache_peer",
        "cache_peer_access", "cache_replacement_policy", "cache_stoplist",
        "cache_stoplist_pattern", "cache_store_log", "cache_swap",
        "cache_swap_high", "cache_swap_log", "cache_swap_low", "client_db",
        "client_lifetime", "client_netmask", "connect_timeout", "coredump_dir",
        "dead_peer_timeout", "debug_options", "delay_access", "delay_class",
        "delay_initial_bucket_level", "delay_parameters", "delay_pools",
        "deny_info", "dns_children", "dns_defnames", "dns_nameservers",
        "dns_testnames", "emulate_httpd_log", "err_html_text",
        "fake_user_agent", "firewall_ip", "forwarded_for", "forward_snmpd_port",
        "fqdncache_size", "ftpget_options", "ftpget_program", "ftp_list_width",
        "ftp_passive", "ftp_user", "half_closed_clients", "header_access",
        "header_replace", "hierarchy_stoplist", "high_response_time_warning",
        "high_page_fault_warning", "hosts_file", "htcp_port", "http_access",
        "http_anonymizer", "httpd_accel", "httpd_accel_host",
        "httpd_accel_port", "httpd_accel_uses_host_header",
        "httpd_accel_with_proxy", "http_port", "http_reply_access",
        "icp_access", "icp_hit_stale", "icp_port", "icp_query_timeout",
        "ident_lookup", "ident_lookup_access", "ident_timeout",
        "incoming_http_average", "incoming_icp_average", "inside_firewall",
        "ipcache_high", "ipcache_low", "ipcache_size", "local_domain",
        "local_ip", "logfile_rotate", "log_fqdn", "log_icp_queries",
        "log_mime_hdrs", "maximum_object_size", "maximum_single_addr_tries",
        "mcast_groups", "mcast_icp_query_timeout", "mcast_miss_addr",
        "mcast_miss_encode_key", "mcast_miss_port", "memory_pools",
        "memory_pools_limit", "memory_replacement_policy", "mime_table",
        "min_http_poll_cnt", "min_icp_poll_cnt", "minimum_direct_hops",
        "minimum_object_size", "minimum_retry_timeout", "miss_access",
        "negative_dns_ttl", "negative_ttl", "neighbor_timeout",
        "neighbor_type_domain", "netdb_high", "netdb_low", "netdb_ping_period",
        "netdb_ping_rate", "never_direct", "no_cache", "passthrough_proxy",
        "pconn_timeout", "pid_filename", "pinger_program", "positive_dns_ttl",
        "prefer_direct", "proxy_auth", "proxy_auth_realm", "query_icmp",
        "quick_abort", "quick_abort_max", "quick_abort_min",
        "quick_abort_pct", "range_offset_limit", "read_timeout",
        "redirect_children", "redirect_program",
        "redirect_rewrites_host_header", "reference_age",
        "refresh_pattern", "reload_into_ims", "request_body_max_size",
        "request_size", "request_timeout", "shutdown_lifetime",
        "single_parent_bypass", "siteselect_timeout", "snmp_access",
        "snmp_incoming_address", "snmp_port", "source_ping", "ssl_proxy",
        "store_avg_object_size", "store_objects_per_bucket",
        "strip_query_terms", "swap_level1_dirs", "swap_level2_dirs",
        "tcp_incoming_address", "tcp_outgoing_address", "tcp_recv_bufsize",
        "test_reachability", "udp_hit_obj", "udp_hit_obj_size",
        "udp_incoming_address", "udp_outgoing_address", "unique_hostname",
        "unlinkd_program", "uri_whitespace", "useragent_log",
        "visible_hostname", "wais_relay", "wais_relay_host", "wais_relay_port",
    )

    opts = (
        "proxy-only", "weight", "ttl", "no-query", "default", "round-robin",
        "multicast-responder", "on", "off", "all", "deny", "allow", "via",
        "parent", "no-digest", "heap", "lru", "realm", "children", "q1", "q2",
        "credentialsttl", "none", "disable", "offline_toggle", "diskd",
    )

    actions = (
        "shutdown", "info", "parameter", "server_list", "client_list",
        r'squid.conf',
    )

    actions_stats = (
        "objects", "vm_objects", "utilization", "ipcache", "fqdncache", "dns",
        "redirector", "io", "reply_headers", "filedescriptors", "netdb",
    )

    actions_log = ("status", "enable", "disable", "clear")

    acls = (
        "url_regex", "urlpath_regex", "referer_regex", "port", "proto",
        "req_mime_type", "rep_mime_type", "method", "browser", "user", "src",
        "dst", "time", "dstdomain", "ident", "snmp_community",
    )

    ip_re = (
        r'(?:(?:(?:[3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}|0x0*[0-9a-f]{1,2}|'
        r'0+[1-3]?[0-7]{0,2})(?:\.(?:[3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}|'
        r'0x0*[0-9a-f]{1,2}|0+[1-3]?[0-7]{0,2})){3})|(?!.*::.*::)(?:(?!:)|'
        r':(?=:))(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)){6}(?:[0-9a-f]{0,4}'
        r'(?:(?<=::)|(?<!::):)[0-9a-f]{0,4}(?:(?<=::)|(?<!:)|(?<=:)(?<!::):)|'
        r'(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-4]|2[0-4]\d|1\d\d|'
        r'[1-9]?\d)){3}))'
    )

    tokens = {
        'root': [
            (r'\s+', Whitespace),
            (r'#', Comment, 'comment'),
            (words(keywords, prefix=r'\b', suffix=r'\b'), Keyword),
            (words(opts, prefix=r'\b', suffix=r'\b'), Name.Constant),
            # Actions
            (words(actions, prefix=r'\b', suffix=r'\b'), String),
            (words(actions_stats, prefix=r'stats/', suffix=r'\b'), String),
            (words(actions_log, prefix=r'log/', suffix=r'='), String),
            (words(acls, prefix=r'\b', suffix=r'\b'), Keyword),
            (ip_re + r'(?:/(?:' + ip_re + r'|\b\d+\b))?', Number.Float),
            (r'(?:\b\d+\b(?:-\b\d+|%)?)', Number),
            (r'\S+', Text),
        ],
        'comment': [
            (r'\s*TAG:.*', String.Escape, '#pop'),
            (r'.+', Comment, '#pop'),
            default('#pop'),
        ],
    }


class NginxConfLexer(RegexLexer):
    """
    Lexer for `Nginx <http://nginx.net/>`_ configuration files.

    .. versionadded:: 0.11
    """
    name = 'Nginx configuration file'
    aliases = ['nginx']
    filenames = ['nginx.conf']
    mimetypes = ['text/x-nginx-conf']

    tokens = {
        'root': [
            (r'(include)(\s+)([^\s;]+)', bygroups(Keyword, Whitespace, Name)),
            (r'[^\s;#]+', Keyword, 'stmt'),
            include('base'),
        ],
        'block': [
            (r'\}', Punctuation, '#pop:2'),
            (r'[^\s;#]+', Keyword.Namespace, 'stmt'),
            include('base'),
        ],
        'stmt': [
            (r'\{', Punctuation, 'block'),
            (r';', Punctuation, '#pop'),
            include('base'),
        ],
        'base': [
            (r'#.*\n', Comment.Single),
            (r'on|off', Name.Constant),
            (r'\$[^\s;#()]+', Name.Variable),
            (r'([a-z0-9.-]+)(:)([0-9]+)',
             bygroups(Name, Punctuation, Number.Integer)),
            (r'[a-z-]+/[a-z-+]+', String),  # mimetype
            # (r'[a-zA-Z._-]+', Keyword),
            (r'[0-9]+[km]?\b', Number.Integer),
            (r'(~)(\s*)([^\s{]+)', bygroups(Punctuation, Whitespace, String.Regex)),
            (r'[:=~]', Punctuation),
            (r'[^\s;#{}$]+', String),  # catch all
            (r'/[^\s;#]*', Name),  # pathname
            (r'\s+', Whitespace),
            (r'[$;]', Text),  # leftover characters
        ],
    }


class LighttpdConfLexer(RegexLexer):
    """
    Lexer for `Lighttpd <http://lighttpd.net/>`_ configuration files.

    .. versionadded:: 0.11
    """
    name = 'Lighttpd configuration file'
    aliases = ['lighttpd', 'lighty']
    filenames = ['lighttpd.conf']
    mimetypes = ['text/x-lighttpd-conf']

    tokens = {
        'root': [
            (r'#.*\n', Comment.Single),
            (r'/\S*', Name),  # pathname
            (r'[a-zA-Z._-]+', Keyword),
            (r'\d+\.\d+\.\d+\.\d+(?:/\d+)?', Number),
            (r'[0-9]+', Number),
            (r'=>|=~|\+=|==|=|\+', Operator),
            (r'\$[A-Z]+', Name.Builtin),
            (r'[(){}\[\],]', Punctuation),
            (r'"([^"\\]*(?:\\.[^"\\]*)*)"', String.Double),
            (r'\s+', Whitespace),
        ],

    }


class DockerLexer(RegexLexer):
    """
    Lexer for `Docker <http://docker.io>`_ configuration files.

    .. versionadded:: 2.0
    """
    name = 'Docker'
    aliases = ['docker', 'dockerfile']
    filenames = ['Dockerfile', '*.docker']
    mimetypes = ['text/x-dockerfile-config']

    _keywords = (r'(?:MAINTAINER|EXPOSE|WORKDIR|USER|STOPSIGNAL)')
    _bash_keywords = (r'(?:RUN|CMD|ENTRYPOINT|ENV|ARG|LABEL|ADD|COPY)')
    _lb = r'(?:\s*\\?\s*)'  # dockerfile line break regex
    flags = re.IGNORECASE | re.MULTILINE

    tokens = {
        'root': [
            (r'#.*', Comment),
            (r'(FROM)([ \t]*)(\S*)([ \t]*)(?:(AS)([ \t]*)(\S*))?',
             bygroups(Keyword, Whitespace, String, Whitespace, Keyword, Whitespace, String)),
            (r'(ONBUILD)(\s+)(%s)' % (_lb,), bygroups(Keyword, Whitespace, using(BashLexer))),
            (r'(HEALTHCHECK)(\s+)((%s--\w+=\w+%s)*)' % (_lb, _lb),
                bygroups(Keyword, Whitespace, using(BashLexer))),
            (r'(VOLUME|ENTRYPOINT|CMD|SHELL)(\s+)(%s)(\[.*?\])' % (_lb,),
                bygroups(Keyword, Whitespace, using(BashLexer), using(JsonLexer))),
            (r'(LABEL|ENV|ARG)(\s+)((%s\w+=\w+%s)*)' % (_lb, _lb),
                bygroups(Keyword, Whitespace, using(BashLexer))),
            (r'(%s|VOLUME)\b(\s+)(.*)' % (_keywords), bygroups(Keyword, Whitespace, String)),
            (r'(%s)(\s+)' % (_bash_keywords,), bygroups(Keyword, Whitespace)),
            (r'(.*\\\n)*.+', using(BashLexer)),
        ]
    }


class TerraformLexer(ExtendedRegexLexer):
    """
    Lexer for `terraformi .tf files <https://www.terraform.io/>`_.

    .. versionadded:: 2.1
    """

    name = 'Terraform'
    aliases = ['terraform', 'tf']
    filenames = ['*.tf']
    mimetypes = ['application/x-tf', 'application/x-terraform']

    classes = ('backend', 'data', 'module', 'output', 'provider',
             'provisioner', 'resource', 'variable')
    classes_re = "({})".format(('|').join(classes))

    types = ('string', 'number', 'bool', 'list', 'tuple', 'map', 'set', 'object', 'null')

    numeric_functions = ('abs', 'ceil', 'floor', 'log', 'max',
                         'mix', 'parseint', 'pow', 'signum')

    string_functions = ('chomp', 'format', 'formatlist', 'indent',
                        'join', 'lower', 'regex', 'regexall', 'replace',
                        'split', 'strrev', 'substr', 'title', 'trim',
                        'trimprefix', 'trimsuffix', 'trimspace', 'upper'
                        )

    collection_functions = ('alltrue', 'anytrue', 'chunklist', 'coalesce',
                            'coalescelist', 'compact', 'concat', 'contains',
                            'distinct', 'element', 'flatten', 'index', 'keys',
                            'length', 'list', 'lookup', 'map', 'matchkeys',
                            'merge', 'range', 'reverse', 'setintersection',
                            'setproduct', 'setsubtract', 'setunion', 'slice',
                            'sort', 'sum', 'transpose', 'values', 'zipmap'
                            )

    encoding_functions = ('base64decode', 'base64encode', 'base64gzip',
                          'csvdecode', 'jsondecode', 'jsonencode', 'textdecodebase64',
                          'textencodebase64', 'urlencode', 'yamldecode', 'yamlencode')


    filesystem_functions = ('abspath', 'dirname', 'pathexpand', 'basename',
                            'file', 'fileexists', 'fileset', 'filebase64', 'templatefile')

    date_time_functions = ('formatdate', 'timeadd', 'timestamp')

    hash_crypto_functions = ('base64sha256', 'base64sha512', 'bcrypt', 'filebase64sha256',
                             'filebase64sha512', 'filemd5', 'filesha1', 'filesha256', 'filesha512',
                             'md5', 'rsadecrypt', 'sha1', 'sha256', 'sha512', 'uuid', 'uuidv5')

    ip_network_functions = ('cidrhost', 'cidrnetmask', 'cidrsubnet', 'cidrsubnets')

    type_conversion_functions = ('can', 'defaults', 'tobool', 'tolist', 'tomap',
                                 'tonumber', 'toset', 'tostring', 'try')

    builtins = numeric_functions + string_functions + collection_functions + encoding_functions +\
        filesystem_functions + date_time_functions + hash_crypto_functions + ip_network_functions +\
        type_conversion_functions
    builtins_re = "({})".format(('|').join(builtins))

    def heredoc_callback(self, match, ctx):
        # Parse a terraform heredoc
        # match: 1 = <<[-]?, 2 = name 3 = rest of line

        start = match.start(1)
        yield start, Operator, match.group(1)        # <<[-~]?
        yield match.start(2), String.Delimiter, match.group(2) # heredoc name

        ctx.pos = match.start(3)
        ctx.end = match.end(3)
        yield ctx.pos, String.Heredoc, match.group(3)
        ctx.pos = match.end()

        hdname = match.group(2)
        tolerant = match.group(1)[-1] == "-"

        lines = []
        line_re = re.compile('.*?\n')

        for match in line_re.finditer(ctx.text, ctx.pos):
            if tolerant:
                check = match.group().strip()
            else:
                check = match.group().rstrip()
            if check == hdname:
                for amatch in lines:
                    yield amatch.start(), String.Heredoc, amatch.group()
                yield match.start(), String.Delimiter, match.group()
                ctx.pos = match.end()
                break
            else:
                lines.append(match)
        else:
            # end of heredoc not found -- error!
            for amatch in lines:
                yield amatch.start(), Error, amatch.group()
        ctx.end = len(ctx.text)

    tokens = {
        'root': [
            include('basic'),
            include('whitespace'),

            # Strings
            (r'(".*")', bygroups(String.Double)),

            # Constants
            (words(('true', 'false'), prefix=r'\b', suffix=r'\b'), Name.Constant),

            # Types
            (words(types, prefix=r'\b', suffix=r'\b'), Keyword.Type),

            include('identifier'),
            include('punctuation'),
            (r'[0-9]+', Number),
        ],
        'basic': [
            (r'\s*/\*', Comment.Multiline, 'comment'),
            (r'\s*#.*\n', Comment.Single),
            include('whitespace'),

            # e.g. terraform {
            # e.g. egress {
            (r'(\s*)([0-9a-zA-Z-_]+)(\s*)(=?)(\s*)(\{)',
             bygroups(Whitespace, Name.Builtin, Whitespace, Operator, Whitespace, Punctuation)),

            # Assignment with attributes, e.g. something = ...
            (r'(\s*)([0-9a-zA-Z-_]+)(\s*)(=)(\s*)',
             bygroups(Whitespace, Name.Attribute, Whitespace, Operator, Whitespace)),

            # Assignment with environment variables and similar, e.g. "something" = ...
            # or key value assignment, e.g. "SlotName" : ...
            (r'(\s*)("\S+")(\s*)([=:])(\s*)',
             bygroups(Whitespace, Literal.String.Double, Whitespace, Operator, Whitespace)),

            # Functions, e.g. jsonencode(element("value"))
            (builtins_re + r'(\()', bygroups(Name.Function, Punctuation)),

            # List of attributes, e.g. ignore_changes = [last_modified, filename]
            (r'(\[)([a-z_,\s]+)(\])', bygroups(Punctuation, Name.Builtin, Punctuation)),

            # e.g. resource "aws_security_group" "allow_tls" {
            # e.g. backend "consul" {
            (classes_re + r'(\s+)', bygroups(Keyword.Reserved, Whitespace), 'blockname'),

            # here-doc style delimited strings
            (
                r'(<<-?)\s*([a-zA-Z_]\w*)(.*?\n)',
                heredoc_callback,
            )
        ],
        'blockname': [
            # e.g. resource "aws_security_group" "allow_tls" {
            # e.g. backend "consul" {
            (r'(\s*)("[0-9a-zA-Z-_]+")?(\s*)("[0-9a-zA-Z-_]+")(\s+)(\{)',
             bygroups(Whitespace, Name.Class, Whitespace, Name.Variable, Whitespace, Punctuation)),
        ],
        'identifier': [
            (r'\b(var\.[0-9a-zA-Z-_\.\[\]]+)\b', bygroups(Name.Variable)),
            (r'\b([0-9a-zA-Z-_\[\]]+\.[0-9a-zA-Z-_\.\[\]]+)\b', bygroups(Name.Variable)),
        ],
        'punctuation': [
            (r'[\[\]()\{\},.?:!=]', Punctuation),
        ],
        'comment': [
            (r'[^*/]', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline)
        ],
        'whitespace': [
            (r'\n', Whitespace),
            (r'\s+', Whitespace),
            (r'(\\)(\n)', bygroups(Text, Whitespace)),
        ],
    }


class TermcapLexer(RegexLexer):
    """
    Lexer for termcap database source.

    This is very simple and minimal.

    .. versionadded:: 2.1
    """
    name = 'Termcap'
    aliases = ['termcap']
    filenames = ['termcap', 'termcap.src']
    mimetypes = []

    # NOTE:
    #   * multiline with trailing backslash
    #   * separator is ':'
    #   * to embed colon as data, we must use \072
    #   * space after separator is not allowed (mayve)
    tokens = {
        'root': [
            (r'^#.*', Comment),
            (r'^[^\s#:|]+', Name.Tag, 'names'),
            (r'\s+', Whitespace),
        ],
        'names': [
            (r'\n', Whitespace, '#pop'),
            (r':', Punctuation, 'defs'),
            (r'\|', Punctuation),
            (r'[^:|]+', Name.Attribute),
        ],
        'defs': [
            (r'(\\)(\n[ \t]*)', bygroups(Text, Whitespace)),
            (r'\n[ \t]*', Whitespace, '#pop:2'),
            (r'(#)([0-9]+)', bygroups(Operator, Number)),
            (r'=', Operator, 'data'),
            (r':', Punctuation),
            (r'[^\s:=#]+', Name.Class),
        ],
        'data': [
            (r'\\072', Literal),
            (r':', Punctuation, '#pop'),
            (r'[^:\\]+', Literal),  # for performance
            (r'.', Literal),
        ],
    }


class TerminfoLexer(RegexLexer):
    """
    Lexer for terminfo database source.

    This is very simple and minimal.

    .. versionadded:: 2.1
    """
    name = 'Terminfo'
    aliases = ['terminfo']
    filenames = ['terminfo', 'terminfo.src']
    mimetypes = []

    # NOTE:
    #   * multiline with leading whitespace
    #   * separator is ','
    #   * to embed comma as data, we can use \,
    #   * space after separator is allowed
    tokens = {
        'root': [
            (r'^#.*$', Comment),
            (r'^[^\s#,|]+', Name.Tag, 'names'),
            (r'\s+', Whitespace),
        ],
        'names': [
            (r'\n', Whitespace, '#pop'),
            (r'(,)([ \t]*)', bygroups(Punctuation, Whitespace), 'defs'),
            (r'\|', Punctuation),
            (r'[^,|]+', Name.Attribute),
        ],
        'defs': [
            (r'\n[ \t]+', Whitespace),
            (r'\n', Whitespace, '#pop:2'),
            (r'(#)([0-9]+)', bygroups(Operator, Number)),
            (r'=', Operator, 'data'),
            (r'(,)([ \t]*)', bygroups(Punctuation, Whitespace)),
            (r'[^\s,=#]+', Name.Class),
        ],
        'data': [
            (r'\\[,\\]', Literal),
            (r'(,)([ \t]*)', bygroups(Punctuation, Whitespace), '#pop'),
            (r'[^\\,]+', Literal),  # for performance
            (r'.', Literal),
        ],
    }


class PkgConfigLexer(RegexLexer):
    """
    Lexer for `pkg-config
    <http://www.freedesktop.org/wiki/Software/pkg-config/>`_
    (see also `manual page <http://linux.die.net/man/1/pkg-config>`_).

    .. versionadded:: 2.1
    """

    name = 'PkgConfig'
    aliases = ['pkgconfig']
    filenames = ['*.pc']
    mimetypes = []

    tokens = {
        'root': [
            (r'#.*$', Comment.Single),

            # variable definitions
            (r'^(\w+)(=)', bygroups(Name.Attribute, Operator)),

            # keyword lines
            (r'^([\w.]+)(:)',
             bygroups(Name.Tag, Punctuation), 'spvalue'),

            # variable references
            include('interp'),

            # fallback
            (r'\s+', Whitespace),
            (r'[^${}#=:\n.]+', Text),
            (r'.', Text),
        ],
        'interp': [
            # you can escape literal "$" as "$$"
            (r'\$\$', Text),

            # variable references
            (r'\$\{', String.Interpol, 'curly'),
        ],
        'curly': [
            (r'\}', String.Interpol, '#pop'),
            (r'\w+', Name.Attribute),
        ],
        'spvalue': [
            include('interp'),

            (r'#.*$', Comment.Single, '#pop'),
            (r'\n', Whitespace, '#pop'),

            # fallback
            (r'\s+', Whitespace),
            (r'[^${}#\n\s]+', Text),
            (r'.', Text),
        ],
    }


class PacmanConfLexer(RegexLexer):
    """
    Lexer for `pacman.conf
    <https://www.archlinux.org/pacman/pacman.conf.5.html>`_.

    Actually, IniLexer works almost fine for this format,
    but it yield error token. It is because pacman.conf has
    a form without assignment like:

        UseSyslog
        Color
        TotalDownload
        CheckSpace
        VerbosePkgLists

    These are flags to switch on.

    .. versionadded:: 2.1
    """

    name = 'PacmanConf'
    aliases = ['pacmanconf']
    filenames = ['pacman.conf']
    mimetypes = []

    tokens = {
        'root': [
            # comment
            (r'#.*$', Comment.Single),

            # section header
            (r'^(\s*)(\[.*?\])(\s*)$', bygroups(Whitespace, Keyword, Whitespace)),

            # variable definitions
            # (Leading space is allowed...)
            (r'(\w+)(\s*)(=)',
             bygroups(Name.Attribute, Whitespace, Operator)),

            # flags to on
            (r'^(\s*)(\w+)(\s*)$',
             bygroups(Whitespace, Name.Attribute, Whitespace)),

            # built-in special values
            (words((
                '$repo',  # repository
                '$arch',  # architecture
                '%o',     # outfile
                '%u',     # url
                ), suffix=r'\b'),
             Name.Variable),

            # fallback
            (r'\s+', Whitespace), 
            (r'.', Text),
        ],
    }


class AugeasLexer(RegexLexer):
    """
    Lexer for `Augeas <http://augeas.net>`_.

    .. versionadded:: 2.4
    """
    name = 'Augeas'
    aliases = ['augeas']
    filenames = ['*.aug']

    tokens = {
        'root': [
            (r'(module)(\s*)([^\s=]+)', bygroups(Keyword.Namespace, Whitespace, Name.Namespace)),
            (r'(let)(\s*)([^\s=]+)', bygroups(Keyword.Declaration, Whitespace, Name.Variable)),
            (r'(del|store|value|counter|seq|key|label|autoload|incl|excl|transform|test|get|put)(\s+)', bygroups(Name.Builtin, Whitespace)),
            (r'(\()([^:]+)(\:)(unit|string|regexp|lens|tree|filter)(\))', bygroups(Punctuation, Name.Variable, Punctuation, Keyword.Type, Punctuation)),
            (r'\(\*', Comment.Multiline, 'comment'),
            (r'[*+\-.;=?|]', Operator),
            (r'[()\[\]{}]', Operator),
            (r'"', String.Double, 'string'),
            (r'\/', String.Regex, 'regex'),
            (r'([A-Z]\w*)(\.)(\w+)', bygroups(Name.Namespace, Punctuation, Name.Variable)),
            (r'.', Name.Variable),
            (r'\s+', Whitespace),
        ],
        'string': [
            (r'\\.', String.Escape),
            (r'[^"]', String.Double),
            (r'"', String.Double, '#pop'),
        ],
        'regex': [
            (r'\\.', String.Escape),
            (r'[^/]', String.Regex),
            (r'\/', String.Regex, '#pop'),
        ],
        'comment': [
            (r'[^*)]', Comment.Multiline),
            (r'\(\*', Comment.Multiline, '#push'),
            (r'\*\)', Comment.Multiline, '#pop'),
            (r'[)*]', Comment.Multiline)
        ],
    }


class TOMLLexer(RegexLexer):
    """
    Lexer for `TOML <https://github.com/toml-lang/toml>`_, a simple language
    for config files.

    .. versionadded:: 2.4
    """

    name = 'TOML'
    aliases = ['toml']
    filenames = ['*.toml', 'Pipfile', 'poetry.lock']

    tokens = {
        'root': [
            # Table
            (r'^(\s*)(\[.*?\])$', bygroups(Whitespace, Keyword)),

            # Basics, comments, strings
            (r'[ \t]+', Whitespace),
            (r'\n', Whitespace),
            (r'#.*?$', Comment.Single),
            # Basic string
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String),
            # Literal string
            (r'\'\'\'(.*)\'\'\'', String),
            (r'\'[^\']*\'', String),
            (r'(true|false)$', Keyword.Constant),
            (r'[a-zA-Z_][\w\-]*', Name),

            # Datetime
            # TODO this needs to be expanded, as TOML is rather flexible:
            # https://github.com/toml-lang/toml#offset-date-time
            (r'\d{4}-\d{2}-\d{2}(?:T| )\d{2}:\d{2}:\d{2}(?:Z|[-+]\d{2}:\d{2})', Number.Integer),

            # Numbers
            (r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?j?', Number.Float),
            (r'\d+[eE][+-]?[0-9]+j?', Number.Float),
            # Handle +-inf, +-infinity, +-nan
            (r'[+-]?(?:(inf(?:inity)?)|nan)', Number.Float),
            (r'[+-]?\d+', Number.Integer),

            # Punctuation
            (r'[]{}:(),;[]', Punctuation),
            (r'\.', Punctuation),

            # Operators
            (r'=', Operator)

        ]
    }

class NestedTextLexer(RegexLexer):
    """
    Lexer for `NextedText <https://nestedtext.org>`_, a human-friendly data 
    format.
    
    .. versionadded:: 2.9
    """

    name = 'NestedText'
    aliases = ['nestedtext', 'nt']
    filenames = ['*.nt']

    _quoted_dict_item = r'^(\s*)({0})(.*?)({0}: ?)(.*?)(\s*)$'

    tokens = {
        'root': [
            (r'^(\s*)(#.*?)$', bygroups(Whitespace, Comment)),
            (r'^(\s*)(>)( ?)(.*?)(\s*)$', bygroups(Whitespace, Punctuation, Whitespace, String, Whitespace)),
            (r'^(\s*)(-)( ?)(.*?)(\s*)$', bygroups(Whitespace, Punctuation, Whitespace, String, Whitespace)),
            (_quoted_dict_item.format("'"), bygroups(Whitespace, Punctuation, Name, Punctuation, String, Whitespace)),
            (_quoted_dict_item.format('"'), bygroups(Whitespace, Punctuation, Name, Punctuation, String, Whitespace)),
            (r'^(\s*)(.*?)(:)( ?)(.*?)(\s*)$', bygroups(Whitespace, Name, Punctuation, Whitespace, String, Whitespace)),
        ],
    }
        

class SingularityLexer(RegexLexer):
    """
    Lexer for `Singularity definition files
    <https://www.sylabs.io/guides/3.0/user-guide/definition_files.html>`_.

    .. versionadded:: 2.6
    """

    name = 'Singularity'
    aliases = ['singularity']
    filenames = ['*.def', 'Singularity']
    flags = re.IGNORECASE | re.MULTILINE | re.DOTALL

    _headers = r'^(\s*)(bootstrap|from|osversion|mirrorurl|include|registry|namespace|includecmd)(:)'
    _section = r'^(%(?:pre|post|setup|environment|help|labels|test|runscript|files|startscript))(\s*)'
    _appsect = r'^(%app(?:install|help|run|labels|env|test|files))(\s*)'

    tokens = {
        'root': [
            (_section, bygroups(Generic.Heading, Whitespace), 'script'),
            (_appsect, bygroups(Generic.Heading, Whitespace), 'script'),
            (_headers, bygroups(Whitespace, Keyword, Text)),
            (r'\s*#.*?\n', Comment),
            (r'\b(([0-9]+\.?[0-9]*)|(\.[0-9]+))\b', Number),
            (r'[ \t]+', Whitespace),
            (r'(?!^\s*%).', Text),
        ],
        'script': [
            (r'(.+?(?=^\s*%))|(.*)', using(BashLexer), '#pop'),
        ],
    }

    def analyse_text(text):
        """This is a quite simple script file, but there are a few keywords
        which seem unique to this language."""
        result = 0
        if re.search(r'\b(?:osversion|includecmd|mirrorurl)\b', text, re.IGNORECASE):
            result += 0.5

        if re.search(SingularityLexer._section[1:], text):
            result += 0.49

        return result
