var $ = require('jQuery'),
    Backbone = require('Backbone'),
    sjcl = require('sjcl');;

module.exports = Backbone.Model.extend({

    url: function() {
        return "/rest/auth";
    },

    defaults: {
        key: '',
        keyHash: '',
        isAuthorized: false
    },

    initialize: function() {
        this.on('change:key', $.debounce(this._verifyKey, 500, this), this);
    },

    _verifyKey: function() {

        var key = this.get('key'),
            keySHA256Digest = sjcl.codec.hex.fromBits(sjcl.hash.sha256.hash(key));

        this.set('isAuthorized', this.get('keyHash') === keySHA256Digest);
    }
});