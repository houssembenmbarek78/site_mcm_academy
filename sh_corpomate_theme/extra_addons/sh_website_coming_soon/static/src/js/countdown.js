odoo.define("sh_website_coming_soon.countdown", function (require) {
    "use strict";

    const core = require("web.core");
    const publicWidget = require("web.public.widget");

    const qweb = core.qweb;
    const _t = core._t;

    const ShWebsiteCommingSoonCountDown = publicWidget.Widget.extend({
        selector: ".js_cls_sh_w_comming_soon",
        disabledInEditableMode: true,

        /**
         * @override
         */
        start: function () {
            var launch_date = this.el.dataset.launchDate;
            launch_date = String(launch_date);
            launch_date = launch_date.trim();

            var endTime = new Date(launch_date);
            this.endTime = Date.parse(endTime) / 1000;

            this._updateTimeLeft();
            this._render();
            this.setInterval = setInterval(this._render.bind(this), 1000);
            return this._super(...arguments);
        },
        /**
         * @override
         */

        destroy: function () {
            if (this.setInterval) {
                clearInterval(this.setInterval);
            }
            this._super(...arguments);
        },

        /**
         * Updates the remaining time difference.
         *
         * @private
         */
        _updateTimeLeft: function () {
            var now = new Date();
            now = Date.parse(now) / 1000;
            var timeLeft = this.endTime - now;
            this.timeLeft = timeLeft;
        },

        /**
         * Draws the whole countdown
         *
         * @private
         */
        _render: function () {
            this._updateTimeLeft();
            var days = Math.floor(this.timeLeft / 86400);
            var hours = Math.floor((this.timeLeft - days * 86400) / 3600);
            var minutes = Math.floor((this.timeLeft - days * 86400 - hours * 3600) / 60);
            var seconds = Math.floor(this.timeLeft - days * 86400 - hours * 3600 - minutes * 60);
            days = Math.abs(days);

            if (hours < "10") {
                hours = "0" + hours;
            }
            if (minutes < "10") {
                minutes = "0" + minutes;
            }
            if (seconds < "10") {
                seconds = "0" + seconds;
            }

            this.$(".js_cls_days_count").html(days);
            this.$(".js_cls_hours_count").html(hours);
            this.$(".js_cls_minutes_count").html(minutes);
            this.$(".js_cls_seconds_count").html(seconds);
        },
    });

    publicWidget.registry.ShWebsiteCommingSoonCountDown = ShWebsiteCommingSoonCountDown;

    return ShWebsiteCommingSoonCountDown;
});
