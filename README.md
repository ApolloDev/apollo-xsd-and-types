# apollo-xsd-and-types

## For those simply interested in the XSDs
This repository contains the XSD (XML Schema Definition) for every type defined in the Apollo standard.

The XSDs are found in src/main/resources, their description is as follows:
  * **apollo_types_X.X.X.xsd** - This is the core XSD of the Apollo standard.  It contains types that describe things from the domain of infectious disease transmssion modeling (e.g. epidemics, infectious disease scenarios, control strategies).
  
  * **apollo_service_.X.X.X.xsd** - This XSD defines the messages that are sent to and from the Apollo Broker Service.
  
  * **data_service_.X.X.X.xsd** - This XSD defines the messages that are sent to and from the Data Service.
  
  * **library_service_.X.X.X.xsd** - This XSD defines the messages that are sent to and from the Library Service.
  
  * **services_common_X.X.X.xsd** - This XSD defines messages that are common to all Apollo Services.
  
  * **simulator_service_X.X.X.xsd** - This XSD defines messages that are sent to and from a Simulator Service running on the Apollo network.
  
  * **synthetic_population_service_X.X.X.xsd** - This XSD defines messages that are sent to and from a Synthetic Population Service running on the Apollo Network.
  
  * **visualizer_service_X.X.X.xsd** - This XSD defines messages that are sent to and from a Visualizer Service running on the Apollo Network.
  
## Java Developers

This also a software project that can be built using the Maven.  Running "mvn clean install" will use JAXB to create java types from XSDs.  You can then import this jar as a dependency into your project and use these types.
