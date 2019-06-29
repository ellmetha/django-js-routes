/* eslint-disable */

const routes = {{ routes|safe }};
{% include "js_routes/_base/resolver.js" with var_assignment='const reverseUrl ' routes_var='routes' %}

export default reverseUrl;
