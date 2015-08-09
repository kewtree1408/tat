var App = require('App'),
    BaseView = require('views/base-view');

module.exports = BaseView.extend({

    name: 'auth',

    tpl: require('tpl/auth'),

    initialize: function() {
        this.listenTo(this.model, "change:isAuthorized", this.unlock);
        return this.constructor.__super__.initialize.apply(this, arguments);
    },

    getTemplateData: function() {
        var data = this.constructor.__super__.getTemplateData.apply(this, arguments);
        return _.extend(data, {
            isFirst: data.id === 0
        });
    },

    unlock: function(model, isAuthorized) {

        var lockState = isAuthorized ? 'fa-unlock' : 'fa-lock';

        this.$elem('lock').removeClass('fa-lock fa-unlock').addClass(lockState);

        if (isAuthorized) {
            this.$elem('key-input').attr('disabled', true);
            App.setAuthKey(this.model.get('key'));
        }

        this.$elem('login').attr('disabled', !isAuthorized);
    },

    events: {
        'input .view-auth__key-input': '_onKeyInput',
        'click button' : '_onButtonCLick'
    },

    _onKeyInput: function() {
        var value = this.$elem('key-input').val();
        this.model.set('key', value);
    },

    _onButtonCLick: function() {
        App.go('level/0') ;
    }
});