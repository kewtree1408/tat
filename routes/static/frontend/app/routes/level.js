module.exports = function(level) {

    var App               = require('App'),
        ViewLevel         = require('views/level'),
        ViewError         = require('views/error');

    if (isNaN(level)) {
        throw new Error('Invalid level index');
    }

    var levelNumber = parseInt(level, 10) + 1;

    var levelModel = App.getQuestCollection().add({
        id: level,
        title: 'Level ' + levelNumber
    });

    levelModel.fetch()
        .done(function() {
            App.setContent(new ViewLevel({
                model: levelModel
            }));
        })
        .fail(function() {
            App.getQuestCollection().remove(levelModel);
            App.setContent(new ViewError());
        });
};
