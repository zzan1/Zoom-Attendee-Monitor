// ==UserScript==
// @name         getZoomAttendee
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://zoom.com.cn/*
// @match        https://*.zoom.us/*
// @grant        none
// ==/UserScript==

(function () {
    (function () {
        "use strict";

        let getName = function () {
            let attendeeName = document.getElementsByClassName(
                "participants-item__display-name"
            );
            return attendeeName.length === 0 ? "" : [...attendeeName];
        };

        let date = function date() {
            var date = new Date();
            var month = date.getMonth() + 1; //js从0开始取
            var date1 = date.getDate();
            var hour = date.getHours();
            var minutes = date.getMinutes();
            return month + "-" + date1 + "-" + hour + "-" + minutes;
        };

        let saveTextAsFile = function (text, fileName) {
            const blob = new Blob([...text], { type: "text/plain" });
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = fileName;
            a.click();
            Url.revokeObjectURL();
            a.remove();
        };

        let main = function main() {
            let attendeeName = getName();
            if (attendeeName !== "") {
                let content = [];
                for (let i = 0; i < attendeeName.length; i++) {
                    content.push(attendeeName[i].innerHTML);
                    content.push("\n");
                }
                let fileName = date() + ".txt";
                saveTextAsFile(content, fileName);
            } else {
                console.log(`Can't detect the participants name!`);
                return;
            }
        };
        setInterval(main, 1000 * 60 * 1);
    })();

})();