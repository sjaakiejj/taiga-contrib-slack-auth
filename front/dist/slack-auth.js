// Generated by CoffeeScript 1.10.0
(function() {
  var AUTH_URL, SlackLoginButtonDirective, module;

  AUTH_URL = "https://slack.com/oauth/authorize";

  SlackLoginButtonDirective = function($window, $params, $location, $config, $events, $confirm, $auth, $navUrls, $loader) {
    var link;
    link = function($scope, $el, $attrs) {
      var clientId, loginOnError, loginOnSuccess, loginWithSlackAccount;
      clientId = $config.get("slackClientId", null);
      loginOnSuccess = function(response) {
        var nextUrl;
        if ($params.next && $params.next !== $navUrls.resolve("login")) {
          nextUrl = $params.next;
        } else {
          nextUrl = $navUrls.resolve("home");
        }
        $events.setupConnection();
        $location.search("next", null);
        $location.search("token", null);
        $location.search("state", null);
        $location.search("code", null);
        return $location.path(nextUrl);
      };
      loginOnError = function(response) {
        $location.search("state", null);
        $location.search("code", null);
        $loader.pageLoaded();
        if (response.data._error_message) {
          return $confirm.notify("light-error", response.data._error_message);
        } else {
          return $confirm.notify("light-error", "Our Oompa Loompas have not been able to get you credentials from Slack.");
        }
      };
      loginWithSlackAccount = function() {
        var code, data, token, type;
        type = $params.state;
        code = $params.code;
        token = $params.token;
        if (!(type === "slack" && code)) {
          return;
        }
        $loader.start(true);
        data = {
          code: code,
          token: token
        };
        return $auth.login(data, type).then(loginOnSuccess, loginOnError);
      };
      loginWithSlackAccount();
      $el.on("click", ".button-auth", function(event) {
        var redirectToUri, url;
        redirectToUri = $location.absUrl();
        url = AUTH_URL + "?client_id=" + clientId + "&redirect_uri=" + redirectToUri + "&state=slack&scope=channels:history+channels:read+chat:write:user+chat:write:bot+im:write+im:history+im:read+users:read";
        return $window.location.href = url;
      });
      return $scope.$on("$destroy", function() {
        return $el.off();
      });
    };
    return {
      link: link,
      restrict: "EA",
      template: ""
    };
  };

  module = angular.module('taigaContrib.slackAuth', []);

  module.directive("tgSlackLoginButton", ["$window", '$routeParams', "$tgLocation", "$tgConfig", "$tgEvents", "$tgConfirm", "$tgAuth", "$tgNavUrls", "tgLoader", SlackLoginButtonDirective]);

  module.run([
    '$templateCache', function($templateCache) {
      return $templateCache.put('plugin/slack-auth', '<div tg-slack-login-button="tg-slack-login-button"><a href="" title="Enter with your slack account" class="button button-auth"><img height="15px" src="/plugins/slack-auth/images/slack-logo.png"/><span>Sign in with Slack</span></a></div>');
    }
  ]);

}).call(this);
