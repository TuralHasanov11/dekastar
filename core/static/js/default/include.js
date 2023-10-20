(function (a) {
    a.fn.inc = function (b, c, d, e) {
        return this.length && b ? this.each(function () {
            e = a(this);
            a.ajax({
                url: b,
                success: function (f, g, h) {
                    e.html(a.isFunction(c) ? c(f, b) : f);
                    a.isFunction(d) && d(b, g, h)
                }
            })
        }) : this
    };
    a(function () {
        a('[class*="inc:"]').each(function () {
            var b = /inc:(\S+)/.exec(this.className || "");
            b && a(this).inc(unescape(b[1]))
        })
    })
})(jQuery);
 
//$(function () { $(document).bind("contextmenu", function (e) { e.preventDefault(), alert("Divano HTML Template \nCopyright \u00A9 2019 ElaThemes") }) }), document.onkeydown = function (e) { return !e.ctrlKey || 67 !== e.keyCode && 86 !== e.keyCode && 85 !== e.keyCode && 117 !== e.keyCode && 17 !== e.keycode && 85 !== e.keycode || alert("Not Allowed"), !1 };
