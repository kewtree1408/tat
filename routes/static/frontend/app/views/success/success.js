var App = require('App'),
    BaseView = require('views/base-view');

module.exports = BaseView.extend({

    name: 'success',

    tpl: require('tpl/success')

});