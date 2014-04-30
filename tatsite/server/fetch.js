var Iconv, cheerio, get_children, get_url, iconv, request, urllib;

cheerio = require('cheerio');
request = require('request');
Iconv = require('iconv').Iconv;
urllib = require('url');
iconv = new Iconv('windows-1251', 'utf-8');

get_url = function(url, callback) {
  url = urllib.resolve("http://www.mosgortrans.org/pass3/simplified.php", url);
  console.log("Get url " + url);
  return request({
    url: url,
    encoding: 'binary'
  }, (function(_this) {
    return function(error, response, body) {
      var e;
      body = new Buffer(body, 'binary');
      try {
        body = iconv.convert(body).toString();
      } catch (_error) {
        e = _error;
        console.log(e);
        return;
      }
      return callback(body);
    };
  })(this));
};

get_children = function(url, callback) {
  return get_url(url, function(body) {
    var $;
    $ = cheerio.load(body);
    return $('li').children('a').each(function(e, a) {
      var href, name;
      href = a.attribs.href;
      name = $(this).text();
      return callback(href, name);
    });
  });
};

get_children("simplified.php", function(path, name) {
  var type;
  type = name;
  return get_children(path, function(path, name) {
    var number;
    number = name;
    return get_children(path, function(path, name) {
      var days;
      days = name;
      return get_children(path, function(path, name) {
        var direction;
        direction = name;
        return get_children(path, function(path, name) {
          var stop;
          stop = name;
          return console.log(type, number, days, direction, stop);
        });
      });
    });
  });
});
