(function() {
    "use strict";
  
    var app = angular.module("myApp", ["ngTable", "ngTableDemos"]);
  
    app.controller("demoController", demoController);
    demoController.$inject = ["NgTableParams", "ngTableSimpleMediumList"];
  
    function demoController(NgTableParams, simpleList) {
      this.defaultConfigTableParams = new NgTableParams({}, { dataset: simpleList});
      this.customConfigParams = createUsingFullOptions();
  
      function createUsingFullOptions() {
        var initialParams = {
          count: 5 // initial page size
        };
        var initialSettings = {
          // page size buttons (right set of buttons in demo)
          counts: [],
          // determines the pager buttons (left set of buttons in demo)
          paginationMaxBlocks: 13,
          paginationMinBlocks: 2,
          dataset: simpleList
        };
        return new NgTableParams(initialParams, initialSettings);
      }
    }
  })();