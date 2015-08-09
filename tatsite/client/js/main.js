(function() {
  (function() {
    "use strict";
    var Waypoint, WaypointList, WaypointListApp, WaypointListView, WaypointModal, WaypointView, Waypoints, tatNumbers, tatStops;
    Waypoint = Backbone.Model.extend({});
    WaypointList = Backbone.Collection.extend({
      model: Waypoint,
      url: "/waypoints.json"
    });
    Waypoints = new WaypointList;
    WaypointModal = Backbone.Modal.extend({
      template: _.template($('#modal-template').html()),
      cancelEl: '.bbm-button'
    });
    WaypointView = Backbone.View.extend({
      tagName: "tr",
      template: _.template($("#waypoint-item-template").html()),
      events: {
        "click td": "showDetails"
      },
      initialize: function() {
        return this.listenTo(this.model, "change", this.render);
      },
      render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
      },
      showDetails: function() {
        var modal;
        modal = new WaypointModal({
          model: this.model
        });
        $('.app').html(modal.render().el);
        return this;
      }
    });
    WaypointListView = Backbone.View.extend({
      el: $("#tatApp"),
      events: {
        "keypress #tatNumber": "onInputKeyPress",
        "keypress #stopName": "onInputKeyPress",
        "change #tatType": "inputChanged",
        "change #tatNumber": "inputChanged",
        "change #day": "inputChanged",
        "click #findBtn": "fetch"
      },
      initialize: function() {
        this.listenTo(Waypoints, "sync", this.render);
        Waypoints.fetch();
        this.main = this.$("#waypointsMain");
        this.tatNumber = this.$("#tatNumber");
        this.stopName = this.$("#stopName");
        this.tatType = this.$("#tatType");
        this.day = this.$("#day");
        return this;
      },
      render: function() {
        $("#waypointsList").html("");
        if (Waypoints.length) {
          this.main.show();
          console.log("Waypoints show & render");
          return Waypoints.each(function(waypoint) {
            var view;
            view = new WaypointView({
              model: waypoint
            });
            return $("#waypointsList").append(view.render().el);
          });
        } else {
          this.main.hide();
          return console.log("Waypoints hide");
        }
      },
      onInputKeyPress: function(e) {
        console.log("onInputKeyPress");
        if (e.keyCode === 13) {
          return this.inputChanged();
        }
      },
      inputChanged: function() {
        console.log("inputChanged");
        if (this.tatNumber.val() || this.stopName.val()) {
          return this.fetch();
        }
      },
      fetch: function() {
        return Waypoints.fetch({
          data: {
            number: this.tatNumber.val(),
            stop: this.stopName.val(),
            type: this.tatType.val(),
            day: this.day.val()
          }
        });
      }
    });
    WaypointListApp = new WaypointListView;
    tatNumbers = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.obj.whitespace,
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      remote: '/suggest/numbers/%QUERY'
    });
    tatNumbers.initialize();
    tatStops = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.obj.whitespace,
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      remote: '/suggest/stops/%QUERY'
    });
    tatStops.initialize();
    $('#tatNumber').typeahead(null, {
      name: 'numbers',
      displayKey: 'number',
      source: tatNumbers.ttAdapter(),
      templates: {
        empty: '',
        suggestion: Handlebars.compile('<p><strong>{{number}}</strong></p>')
      }
    });
    return $('#stopName').typeahead(null, {
      name: 'stops',
      displayKey: 'title',
      source: tatStops.ttAdapter(),
      templates: {
        empty: '',
        suggestion: Handlebars.compile('<p>{{title}}</p>')
      }
    });
  })();

}).call(this);
