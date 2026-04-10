var Vt = /^(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)$/i

Fl = function(e) {
    return kr(Array.from(Ar(e)))
}
function Pt(e) {
    return function(e) {
        if (Array.isArray(e))
            return Ut(e)
    }(e) || function(e) {
        if ("undefined" != typeof Symbol && null != e[Symbol.iterator] || null != e["@@iterator"])
            return Array.from(e)
    }(e) || Dt(e) || function() {
        throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
    }()
}
function Ut(e, t) {
    (null == t || t > e.length) && (t = e.length)
    for (var n = 0, r = new Array(t); n < t; n++)
        r[n] = e[n]
    return r
}
function kr(e) {
    return Pt(e).map((function(e) {
        return String.fromCharCode(e)
    }
    )).join("")
}
function Wt(e) {
    return "string" == typeof e && Vt.test(e)
}
function Yt(e) {
    if (!Wt(e))
        throw TypeError("Invalid UUID")
    var t, n = new Uint8Array(16)
    return n[0] = (t = parseInt(e.slice(0, 8), 16)) >>> 24,
    n[1] = t >>> 16 & 255,
    n[2] = t >>> 8 & 255,
    n[3] = 255 & t,
    n[4] = (t = parseInt(e.slice(9, 13), 16)) >>> 8,
    n[5] = 255 & t,
    n[6] = (t = parseInt(e.slice(14, 18), 16)) >>> 8,
    n[7] = 255 & t,
    n[8] = (t = parseInt(e.slice(19, 23), 16)) >>> 8,
    n[9] = 255 & t,
    n[10] = (t = parseInt(e.slice(24, 36), 16)) / 1099511627776 & 255,
    n[11] = t / 4294967296 & 255,
    n[12] = t >>> 24 & 255,
    n[13] = t >>> 16 & 255,
    n[14] = t >>> 8 & 255,
    n[15] = 255 & t,
    n
}
function Ar(e) {
    return Yt(e)
}
let a = "0184bbb4-4d9d-466a-8502-aa4d4cd168b0"
// a = '09c1c958-8a66-4b95-9ca9-9c332631e011'
// let res = Fl(a)
// console.log(res)