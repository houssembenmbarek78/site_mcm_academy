odoo.define('mcm_website_theme.search', function (require) {
'use strict';

var core = require('web.core');
var config = require('web.config');
var concurrency = require('web.concurrency');
var publicWidget = require('web.public.widget');
var VariantMixin = require('sale.VariantMixin');
var wSaleUtils = require('website_sale.utils');
require("web.zoomodoo");

var qweb = core.qweb;

var _t = core._t;
var timeout;
/**
 * @todo maybe the custom autocomplete logic could be extract to be reusable
 */
publicWidget.registry.statesSearchBar = publicWidget.Widget.extend({
    selector: '.o_mcm_products_searchbar_form',
    xmlDependencies: ['/mcm_website_theme/static/src/xml/homepage_utils.xml'],
    events: {
        'input .state-search-query': '_onInput',
        'focusout': '_onFocusOut',
        'keydown .state-search-query': '_onKeydown',
    },
    autocompleteMinWidth: 300,

    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);

        this._dp = new concurrency.DropPrevious();
        this._onInput = _.debounce(this._onInput, 400);
        this._onFocusOut = _.debounce(this._onFocusOut, 100);
    },
    /**
     * @override
     */
    start: function () {
        this.$input = this.$('.state-search-query');
        this.limit = parseInt(this.$input.data('limit'));
        this.displayDescription = !!this.$input.data('displayDescription');
        this.displayPrice = !!this.$input.data('displayPrice');
        this.displayImage = !!this.$input.data('displayImage');

        if (this.limit) {
            this.$input.attr('autocomplete', 'off');
        }
        return this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _fetch: function () {
        return this._rpc({
            route: '/states/autocomplete',
            params: {
                'term': this.$input.val(),
                'options': {

                },
            },
        });
    },
    /**
     * @private
     */
    _render: function (res) {
        var $prevMenu = this.$menu;
        this.$el.toggleClass('dropdown show', !!res);
        if (res) {
            var states = res['states'];
            this.$menu = $(qweb.render('mcm_website_theme.productsSearchBar.autocomplete', {
                states: states,
//                hasMoreProducts: states.length < res['products_count'],
//                currency: res['currency'],
                widget: this,
            }));
            this.$menu.css('min-width', this.autocompleteMinWidth);
            this.$el.append(this.$menu);
        }
        if ($prevMenu) {
            $prevMenu.remove();
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onInput: function () {
//        if (!this.limit) {
//            return;
//        }
        this._dp.add(this._fetch()).then(this._render.bind(this));
    },
    /**
     * @private
     */
    _onFocusOut: function () {
        if (!this.$el.has(document.activeElement).length) {
            this._render();
        }
    },
    /**
     * @private
     */
    _onKeydown: function (ev) {
        switch (ev.which) {
            case $.ui.keyCode.ESCAPE:
                this._render();
                break;
            case $.ui.keyCode.UP:
                ev.preventDefault();
                this.$menu.children().last().focus();
                break;
            case $.ui.keyCode.DOWN:
                ev.preventDefault();
                this.$menu.children().first().focus();
                break;
        }
    },
});
});