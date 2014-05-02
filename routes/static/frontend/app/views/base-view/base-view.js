var Backbone = require('Backbone'),
    Handlebars = require('Handlebars'),

    FADE_SPEED = 'fast';

module.exports = Backbone.View.extend({

    initialize: function() {

        var classes = ['view'];

        this._name = this.name ? 'view-' + this.name : '';
        classes.push(this._name);
        this.$el.addClass(classes.join(' '));

        this._childView = null;

        if (this.tpl) {
            this.template = Handlebars.compile(this.tpl);
        }
    },

    render: function() {
        if (this.template) {
            this.$el.html(this.template(this.getTemplateData()));
        }
        return this;
    },

    getTemplateData: function() {
        return this.model && this.model.toJSON() || {};
    },

    elemSelector: function(name) {
        return '.' + this._name + '__' + name;
    },

    $elem: function(name) {
        return this.$(this.elemSelector(name));
    },

    setContent: function(view) {

        var _this = this;

        if (this._childView) {
            this._childView.$el.fadeOut(FADE_SPEED, function() {
                _this.swapChildView();
                _this._show(view);
            });
        } else {
            this._childView = view;
            this._show(view);
        }

        return this;
    },

    _show: function(view) {
        var $viewElement = view.render().$el;
        $viewElement.css('display', 'none');
        this.$el.html($viewElement)
        $viewElement.fadeIn(FADE_SPEED);
    },

    swapChildView: function(view) {
        if (this._childView != null) {
            this._childView.remove();
            this._childView = null;
        }
        if (view) {
            this._childView = view;
        }
    },

    remove: function() {
        this.swapChildView();
        return this.constructor.__super__.initialize.apply(this, arguments);
    }

});