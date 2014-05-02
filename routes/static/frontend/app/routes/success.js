module.exports = function() {

    var App          = require('App'),
        ViewIntro    = require('views/success'),
        ViewError    = require('views/error');

    if (App.getAuthKey()) {
        App.setContent(new ViewIntro());
    } else {
        App.setContent(new ViewError());
    }
};