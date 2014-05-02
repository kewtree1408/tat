var $ = require('jQuery'),
    Backbone = require('Backbone');

module.exports = Backbone.Model.extend({

    url: function() {
        return "/rest/page/" + this.get('id');
    },

    defaults: {
        id: 0,
        title: '',
        content: [],
        actions: [],
        isLast: false
    }

});