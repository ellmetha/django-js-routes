window.reverseUrl = (function () {
  const argRegex = /<\w*>/g;

  return function(name) {
    const urlPattern = window.routes[name];
    var url = urlPattern;

    if (!urlPattern) {
      throw "URL '" + name + "' not found";
    }

    if (arguments.length === 0) {
      return url;
    }

    const tokens = urlPattern.match(argRegex);

    if (typeof (arguments[1]) == 'object' && !Array.isArray(arguments[1])) {
      if (tokens) {
        for (var i=0; i < tokens.length; i += 1) {
          const token = tokens[i];
          const argName = token.slice(1, -1);
          const argValue = arguments[1][argName];

          if (argValue === undefined) {
            throw "Argument '" + argName + "' not provided.";
          }
          url = url.replace(token, argValue);
        }
      }
    } else {
      const argsArray = Array.isArray(arguments[1]) ? arguments[1] :
        Array.prototype.slice.apply(arguments, [1, arguments.length]);
      if (tokens) {
        if (tokens.length !== argsArray.length) {
          throw "Wrong number of arguments ; espected " + tokens.length + " arguments.";
        }

        for (var i=0; i < tokens.length; i += 1) {
          const token = tokens[i];
          const argValue = argsArray[i];
          url = url.replace(token, argValue);
        }
      }
    }

    return url;
  };
})();
