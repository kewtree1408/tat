var App = require('App'),
    BaseView = require('views/base-view');

module.exports = BaseView.extend({

    name: 'intro',

    tpl: require('tpl/intro'),

    initialize: function() {
        this.$el.addClass('view-intro_index_' + this.model.get('id'));
        this.listenTo(this.model, "request sync error", this.render);
        return this.constructor.__super__.initialize.apply(this, arguments);
    },

    getTemplateData: function() {
        var data = this.constructor.__super__.getTemplateData.apply(this, arguments);
        return _.extend(data, {
            isFirst: data.id === 0
        });
    },

    events: {
        "click button" : "onButtonCLick"
    },

    onButtonCLick: function() {

        var nextPage;

        if (this.model.get('isLast')) {

            App.go('let-me-in') ;

        } else {

            nextPage = this.model.get('id') + 1;
            App.go('intro/' + nextPage) ;

        }
    }
});