module.exports = function(pageId) {

    var App               = require('App'),
        ModelIntro        = require('models/page'),
        ViewIntro         = require('views/intro');

    pageId = pageId || 0;

    if (isNaN(pageId)) {
        throw new Error('Invalid page index');
    }

    var pageModel = new ModelIntro({
        id: pageId
    });

    App.setContent(new ViewIntro({
        model: pageModel
    }));

    pageModel.fetch();
};
