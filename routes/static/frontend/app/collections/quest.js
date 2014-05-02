var Backbone = require('Backbone'),
    ModelLevel   = require('models/level');

module.exports = Backbone.Collection.extend({

    model: ModelLevel,

    comparator: 'id'

});