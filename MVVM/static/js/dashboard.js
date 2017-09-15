$(document).ready(function(){

    function featureModel() {
      var self = this;
      self.title = ko.observable();
      self.description = ko.observable();
      self.client = ko.observable()
      self.priority = ko.observable()
      self.due = ko.observable()
      self.productArea = ko.observable()
    }

    $.get("/feature-request", function(data, status){
        alert("Data: " + data.title + "\nStatus: " + status);
    });


        
      ko.applyBindings(new featureModel());
    });