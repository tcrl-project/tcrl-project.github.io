#!/usr/bin/env python3
"""Sync Docusaurus runtime JS chunks with the already-updated quickstart HTML copy."""
import re

URL = "https://cloud.tencent.com/product/emr"
MAIL = "tcrl@tencent.com"


def esc(text):
    return "".join(c if ord(c) < 128 else "\\u%04X" % ord(c) for c in text)


def a_mail(jx, c):
    return '(0,%s.jsx)(%s.a,{href:"mailto:%s",children:"%s"})' % (jx, c, MAIL, MAIL)


def a_emr(jx, c, label):
    return ('(0,%s.jsx)(%s.a,{href:"%s",target:"_blank",rel:"noopener",children:"%s"})'
            % (jx, c, URL, esc(label)))


def cn_quickstart(jx, c):
    return ('(0,{jx}.jsxs)({c}.p,{{children:["{t1}",{mail},"{t2}",{emr},"{t3}"]}})').format(
        jx=jx, c=c,
        t1=esc("目前 TCRL 开白体验中，可联系 "),
        mail=a_mail(jx, c),
        t2=esc(" 申请开白后，登录"),
        emr=a_emr(jx, c, "腾讯云弹性 MapReduce（EMR）控制台"),
        t3=esc("获取 API Key 使用，并进行实验管理和用量监控。"),
    )


def en_quickstart(jx, c):
    return ('(0,{jx}.jsxs)({c}.p,{{children:["TCRL is currently in allowlist beta. Contact ",'
            '{mail}," to request access. Once approved, sign in to the ",{emr},'
            '" to get your API Key, manage experiments, and monitor usage."]}})').format(
        jx=jx, c=c, mail=a_mail(jx, c),
        emr=a_emr(jx, c, "Tencent Cloud Elastic MapReduce (EMR) console"))


def cn_experiments(jx, c):
    return '(0,{jx}.jsxs)({c}.p,{{children:["{t1}",{mail},"{t2}"]}})'.format(
        jx=jx, c=c, t1=esc("想贡献实验？联系 "), mail=a_mail(jx, c), t2=esc("。"))


def en_experiments(jx, c):
    return ('(0,{jx}.jsxs)({c}.p,{{children:["Want to contribute an experiment? Contact ",'
            '{mail},"."]}})').format(jx=jx, c=c, mail=a_mail(jx, c))


RX = {
    "cn_quickstart": re.compile(
        r'\(0,(\w+)\.jsxs\)\((\w+)\.p,\{children:\["\\u8BBE\\u7F6E\\u73AF\\u5883\\u53D8\\u91CF'
        r'.*?"\\uFF09\\uFF1A"\]\}\)'),
    "en_quickstart": re.compile(
        r'\(0,(\w+)\.jsxs\)\((\w+)\.p,\{children:\["Set your environment variables '
        r'\(contact us via WeCom to get an API key: ".*?"\):"\]\}\)'),
    "cn_experiments": re.compile(
        r'\(0,(\w+)\.jsxs\)\((\w+)\.p,\{children:\["\\u60F3\\u8D21\\u732E\\u5B9E\\u9A8C'
        r'.*?"\\u3002"\]\}\)'),
    "en_experiments": re.compile(
        r'\(0,(\w+)\.jsxs\)\((\w+)\.p,\{children:\["Want to contribute an experiment\? '
        r'Contact ".*?\\u4FE1\."\]\}\)'),
}

BUILDERS = {
    "cn_quickstart": cn_quickstart,
    "en_quickstart": en_quickstart,
    "cn_experiments": cn_experiments,
    "en_experiments": en_experiments,
}

TARGETS = [
    ("assets/js/cdcf1cd1.d637be4c.js", "cn_quickstart"),
    ("assets/js/b780c31e.f332863a.js", "cn_quickstart"),
    ("assets/js/7a81e2ee.9dda7694.js", "cn_experiments"),
    ("en/assets/js/a4ebee1e.b1be243b.js", "en_quickstart"),
    ("en/assets/js/05be5cd4.1e6f3b0c.js", "en_quickstart"),
    ("en/assets/js/4fef776c.4f3ac5b5.js", "en_experiments"),
]

for path, kind in TARGETS:
    s = open(path, encoding="utf-8").read()
    ms = list(RX[kind].finditer(s))
    assert len(ms) == 1, "anchor count %d in %s (%s)" % (len(ms), path, kind)
    m = ms[0]
    jx, c = m.group(1), m.group(2)
    s = s[:m.start()] + BUILDERS[kind](jx, c) + s[m.end():]
    assert "maximuswang" not in s and "kellancai" not in s, "leftover contact in %s" % path
    assert MAIL in s, "mail missing in %s" % path
    open(path, "w", encoding="utf-8").write(s)
    print("patched %-38s kind=%-15s jsx=%s comp=%s" % (path, kind, jx, c))

print("done")
