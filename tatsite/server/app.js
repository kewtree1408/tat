var MongoClient, app, db_host, express, format, get_route_title, get_times, util, weekday;

format = require('string-format-js');
express = require('express');
MongoClient = require('mongodb').MongoClient;
util = require('util');
app = express();
app.use("/client", express["static"]('../client'));
db_host = "localhost";

get_route_title = function(doc) {
  var type_name;
  type_name = (function() {
    switch (doc.type) {
      case 'avto':
        return "автобус";
      case 'tram':
        return "трамвай";
      case 'trol':
        return "тролейбус";
    }
  })();
  return "" + doc.number + " " + type_name;
};

get_times = function(times) {
  var result, t, _i, _len;
  result = [];
  for (_i = 0, _len = times.length; _i < _len; _i++) {
    t = times[_i];
    result.push('%02d:%02d'.format(t[0], t[1]));
  }
  return result;
};

weekday = function() {
  var today;
  today = new Date();
  switch (today.getDay()) {
    case 0:
      return 7;
    default:
      return today.getDay() - 1;
  }
};

app.get("/waypoints.json", function(req, res) {
  console.log("User query: " + (JSON.stringify(req.query)));
  return MongoClient.connect("mongodb://" + db_host + "/tat", (function(_this) {
    return function(err, db) {
      var query;
      if (err) {
        throw err;
      }
      console.log("Connected to Database");
      query = {};
      if (req.query.day && req.query.day !== "") {
        query.days = parseInt(req.query.day);
      } else {
        query.days = weekday();
      }
      if (req.query.number) {
        query.number = req.query.number;
      }
      if (req.query.stop) {
        query.stop = req.query.stop;
      }
      if (req.query.type) {
        query.type = req.query.type;
      }
      return db.collection("waypoints", function(err, collection) {
        if (err) {
          throw err;
        }
        console.log("DB query: " + (JSON.stringify(query)));
        return collection.find(query).limit(50).toArray(function(err, items) {
          var item, waypoints, _i, _len;
          waypoints = [];
          for (_i = 0, _len = items.length; _i < _len; _i++) {
            item = items[_i];
            waypoints.push({
              route_title: get_route_title(item),
              stop_title: item.stop,
              id: "" + item._id,
              to: item.direction.split(' - ')[1],
              near_times: get_times(item.times.slice(0, 6)),
              all_times: get_times(item.times)
            });
          }
          return res.send(JSON.stringify(waypoints));
        });
      });
    };
  })(this));
});

app.get("/suggest/numbers/:number", function(req, res) {
  console.log("User query: " + (JSON.stringify(req.params)));
  return MongoClient.connect("mongodb://" + db_host + "/tat", (function(_this) {
    return function(err, db) {
      if (err) {
        throw err;
      }
      console.log("Connected to Database");
      return db.collection("waypoints", function(err, collection) {
        if (err) {
          throw err;
        }
        return collection.distinct('number', {
          number: {
            $regex: "" + req.params.number
          }
        }, function(err, items) {
          var item, numbers, _i, _len, _ref;
          numbers = [];
          _ref = items.slice(0, 6);
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            item = _ref[_i];
            numbers.push({
              number: item
            });
          }
          return res.send(JSON.stringify(numbers));
        });
      });
    };
  })(this));
});

app.get("/suggest/stops/:stop", function(req, res) {
  console.log("User query: " + (JSON.stringify(req.params)));
  return MongoClient.connect("mongodb://" + db_host + "/tat", (function(_this) {
    return function(err, db) {
      if (err) {
        throw err;
      }
      console.log("Connected to Database");
      return db.collection("waypoints", function(err, collection) {
        if (err) {
          throw err;
        }
        return collection.distinct('stop', {
          stop: {
            $regex: "" + req.params.stop
          }
        }, function(err, items) {
          var item, stops, _i, _len, _ref;
          stops = [];
          _ref = items.slice(0, 6);
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            item = _ref[_i];
            stops.push({
              title: item
            });
          }
          return res.send(JSON.stringify(stops));
        });
      });
    };
  })(this));
});

app.listen(8000);