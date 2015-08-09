var $ = require('$'),
    Router = require('Router'),
    CollectionQuest = require('collections/quest'),
    ViewPage = require('views/page');

module.exports = (function() {

    var _authKey,
        _router,
        _rootView,
        _questCollection;

    var _setRootView = function() {
        _rootView = new ViewPage();
    };

    var _setRouter = function(router) {
        _router = router;
    };

    return {

        initialize: function() {
            _setRootView();
            _setRouter(new Router());
        },

        getRouter: function() {
            return _router;
        },

        getQuestCollection: function() {
            if (_questCollection) return _questCollection;
            return (_questCollection = new CollectionQuest());
        },

        setContent: function() {
            _rootView.setContent.apply(_rootView, arguments);
        },

        setAuthKey: function(key) {
            _authKey = key;
            return this;
        },

        getAuthKey: function() {
            return _authKey;
        },

        go: function(path) {
            this.getRouter().navigate(path, {
                trigger: true
            });
        }
    }
}());