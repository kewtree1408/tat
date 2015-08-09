var Backbone = require('Backbone'),

    Router = Backbone.Router.extend({

        initialize: function() {
            Backbone.history.start({
                pushState: true
            });
        },

        routes: {
            '':          'intro',
            'tat/:id':   'tat',
            'route/:id': 'route'
        },

        tat:     require('routes/intro'),

        route:      require('routes/auth')
    });

(function () {

    var instance;

    module.exports = function() {

        if (instance) return instance;

        return (instance = new Router());
    };
}());