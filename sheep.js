crypt = require("crypto-js");


// 构建x-tt-params 的参数
function get_param(e) {
    const i = ((e, t) => {
            let i = e.toString();
            const o = i.length;
            return o < 16 ? i = new Array(16 - o + 1).join("0") + i : o > 16 && (i = i.slice(0, 16)),
                i
        }
    )("webapp1.0+20210628")
        , n = crypt.enc.Utf8.parse(i);
    return crypt.AES.encrypt(e, n, {
        iv: n,
        mode: crypt.mode.CBC,
        padding: crypt.pad.Pkcs7
    }).toString()
}


function get_x_tt_params(cursor_, sec_uid, fp) {
    var e = "aid=1988&app_name=tiktok_web&channel=tiktok_web&device_platform=web_pc&device_id=7124993811416286766" +
        "&region=US&priority_region=&os=mac&referer=&root_referer=undefined&cookie_enabled=true&screen_width=1440" +
        "&screen_height=900&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Mozilla&browser_version=" +
        "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" +
        "&browser_online=true&verifyFp=verify_8d9870aa4cdcd81e69d31920f4c4cdd5&app_language=zh-Hant-TW&webcast_language=zh-Hant-TW&tz_name=" +
        "Asia/Shanghai&is_page_visible=true&focus_state=true&is_fullscreen=true&history_len=8&battery_info=0.71&" +
        "from_page=user&secUid=" + sec_uid + "&count=30" +
        "&cursor=" + cursor_ + "&language=zh-Hant-TW&userId=undefined&is_encryption=1"

    // var e = "aid=1988&app_name=tiktok_web&channel=tiktok_web&device_platform=web_pc&device_id=7127178569138079278&region=US&priority_region=&os=mac&referer=&root_referer=undefined&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36&browser_online=true&verifyFp=undefined&app_language=zh-Hant-TW&webcast_language=zh-Hant-TW&tz_name=Asia/Shanghai&is_page_visible=true&focus_state=true&is_fullscreen=true&history_len=9&battery_info=0.9&from_page=user&secUid=MS4wLjABAAAAo21C6uyUY3Ms-gx5Vu5wNM9eIG-3-HErpi-6toZTa9akDtu31OmN5BDDaIp7_lgM&count=30&cursor=1649459392000&language=zh-Hant-TW&userId=undefined&is_encryption=1"
    var result = get_param(e)
    return result
}

a = get_x_tt_params("1649459392000", "MS4wLjABAAAAo21C6uyUY3Ms-gx5Vu5wNM9eIG-3-HErpi-6toZTa9akDtu31OmN5BDDaIp7_lgM")
console.log(a)

