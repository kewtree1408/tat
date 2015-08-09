module.exports = function() {

    var App              = require('App'),
        ModelAuth        = require('models/auth'),
        ViewAuth         = require('views/auth');

    var authModel = new ModelAuth();

    App.setContent(new ViewAuth({
        model: authModel
    }));

    authModel.fetch();
};
