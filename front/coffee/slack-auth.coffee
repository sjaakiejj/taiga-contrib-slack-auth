AUTH_URL = "https://slack.com/oauth/authorize"

SlackLoginButtonDirective = ($window, $params, $location, $config, $events, $confirm,
                              $auth, $navUrls, $loader) ->
    # Login or registar a user with his/her slack account.
    #
    # Example:
    #     tg-slack-login-button()
    #
    # Requirements:
    #   - ...

    link = ($scope, $el, $attrs) ->
        clientId = $config.get("slackClientId", null)

        loginOnSuccess = (response) ->
            if $params.next and $params.next != $navUrls.resolve("login")
                nextUrl = $params.next
            else
                nextUrl = $navUrls.resolve("home")

            $events.setupConnection()

            $location.search("next", null)
            $location.search("token", null)
            $location.search("state", null)
            $location.search("code", null)
            $location.path(nextUrl)

        loginOnError = (response) ->
            $location.search("state", null)
            $location.search("code", null)
            $loader.pageLoaded()

            if response.data._error_message
                $confirm.notify("light-error", response.data._error_message )
            else
                $confirm.notify("light-error", "Our Oompa Loompas have not been able to get you
                                                credentials from Slack.")  #TODO: i18n

        loginWithSlackAccount = ->
            type = $params.state
            code = $params.code
            token = $params.token

            return if not (type == "slack" and code)
            $loader.start(true)

            data = {code: code, token: token}
            $auth.login(data, type).then(loginOnSuccess, loginOnError)

        loginWithSlackAccount()

        $el.on "click", ".button-auth", (event) ->
            redirectToUri = $location.absUrl()
            url = "#{AUTH_URL}?client_id=#{clientId}&redirect_uri=#{redirectToUri}&state=slack&scope=channels:history+channels:read+chat:write:user+chat:write:bot+im:write+im:history+im:read+users:read"
            $window.location.href = url

        $scope.$on "$destroy", ->
            $el.off()

    return {
        link: link
        restrict: "EA"
        template: ""
    }

module = angular.module('taigaContrib.slackAuth', [])
module.directive("tgSlackLoginButton", ["$window", '$routeParams', "$tgLocation", "$tgConfig", "$tgEvents",
                                         "$tgConfirm", "$tgAuth", "$tgNavUrls", "tgLoader",
                                         SlackLoginButtonDirective])
