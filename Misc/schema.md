# MongoDB validation schema for the website logs

The below is the MongoDB [validation schema](https://docs.mongodb.com/manual/core/schema-validation/) for the website event logs collection. This is to be entered in the mongo shell, after selecting the appropriate database. 

```
db.createCollection( "website_logs" , { 
   validator: { $jsonSchema: { 

      bsonType: "object", 

      required: [ "path_info", "referrer", "page_title", "browser_family", "browser_version", "os_family", "os_version", "device_family", "device_type", "method", "event_name", "visited_by", "ip_address", "country", "region", "city", "latitude", "longitude", "datetime", "first_time_visit" ], 
      properties: { 
         path_info: { 
            bsonType: "string", 
            pattern: "^/(.)*",
            description: "Webpage path. Required and must be a string beginning with /"
         }, 
         method: { 
            enum: [ "GET", "POST", "HEAD", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH" ],
            description: "Required and must be a valid HTTP request method"
         }, 
         event_name: { 
            bsonType: "string", 
            pattern: "^event\.(.)+",
            description: "Event name. Required and must be of the form event.(...)"
         }, 
         visited_by: { 
            bsonType: "string", 
            description: "Username of visitor. Required and must be anonymous or a username"
         }, 
         ip_address: { 
            bsonType: "string",
            pattern: "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            description: "A valid IPv4 address. Required."
         },
         country: {
            bsonType: "string",
            description: "Country. Required and must be a country name or Unknown"
         },
         region: {
            bsonType: "string",
            description: "Region. Required and must be a region name or Unknown"
         },
         city: {
            bsonType: "string",
            description: "City. Required and must be a city name or Unknown"
         },
         datetime: {
            bsonType: "date",
            description: "Datetime of log. Required."
         },
         first_time_visit: {
            bsonType: "string",
            description: "Whether the visit was first time ("true") or returning ("false"). Required."
         },
         referrer: {
            bsonType: "string",
            description: "The website which had the link that the user clicked on to visit this URL"
         },
         browser_family: {
            bsonType: "string",
            description: "The family of browsers the user's browser belongs to."
         },
         browser_version: {
            bsonType: "string",
            description: "Version of the user's browser"
         },
         os_family: {
            bsonType: "string",
            description: "Family of operating systems the user's OS belongs to."
         },
         os_version: {
            bsonType: "string",
            description: "Verson of the user's OS."
         },
         device_family: {
            bsonType: "string",
            description: "Family of devices that the user's device belongs to"
         },
         device_type: {
            bsonType: "string",
            description: "Type of device (Mobile/PC/Tablet etc.)"
         },
         latitude: {
            description: "Latitude"
         },
         longitude: {
            description: "Longitude"
         },
         device_type: {
            bsonType: "string",
            description: "Device type. Required."
         },
         view_args: {
            bsonType: "array"
         },
         view_kwargs: {
            bsonType: "object"
         },
         post_data: {
            bsonType: "object"
         },
         },
      }
   }
});
```