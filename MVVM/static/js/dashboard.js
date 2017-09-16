$(document).ready(function(){

    function feature(){
      var self = this
      self.title = ko.observable()
      self.description = ko.observable()
      self.client = ko.observable()
      self.priority = ko.observable()
      self.due = ko.observable()
      self.productArea = ko.observable()
      self.mapProperties = function(data){
        self.title(data.title)
        self.description(data.description)
        self.client(data.client)
        self.priority(data.priority)  
        self.due(data.due)
        self.productArea(data.productArea)  
      }
    }
    
    var app = new featureModel()
    ko.applyBindings(app)

    $.get("/feature-request", function(data, status){
        app.mapProperties(data)
    })    
})