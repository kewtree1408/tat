/**
 * Main view, container for everything else
 * @type {exports}
 */
var Backbone = require('Backbone'),
    BaseView = require('views/base-view');

module.exports = BaseView.extend({

    name: 'page',

    theme: 'light',

    el: 'body',

    initialize: function() {

        if (this.theme) {
            this.$el.addClass('view-page_theme_' + this.theme);
        }

        return this.constructor.__super__.initialize.apply(this, arguments);
    }

});