$(document).ready(function(){

    function featureModel(){
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
        self.due(data.due)
        self.productArea(data.product_area)  
      }
    }
    
    var app = new featureModel()
    ko.applyBindings(app)

    $.get("/feature-request", function(data, status){
        app.mapProperties(data)
    })

    
})