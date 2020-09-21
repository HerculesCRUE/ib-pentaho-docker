package es.um.asio.service.trellis.impl;

import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

import org.apache.http.HttpStatus;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.Resource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;
import org.trellisldp.api.RuntimeTrellisException;

import com.jayway.restassured.RestAssured;
import com.jayway.restassured.response.Response;
import com.jayway.restassured.specification.RequestSpecification;

import es.um.asio.abstractions.domain.ManagementBusEvent;
import es.um.asio.service.trellis.TrellisOperations;
import es.um.asio.service.util.MediaTypes;
import es.um.asio.service.util.RdfObjectMapper;
import es.um.asio.service.util.TrellisUtils;

@Service
public class TrellisOperationsImpl implements TrellisOperations {

	/** The logger. */
    private final Logger logger = LoggerFactory.getLogger(TrellisOperationsImpl.class);
    
    /** The trellis utils. */
    @Autowired
    private TrellisUtils trellisUtils;
    
    /** The trellis url end point. */
    @Value("${app.trellis.endpoint}")
    private String trellisUrlEndPoint;
    
    /** The authentication enabled. */
    @Value("${app.trellis.authentication.enabled:false}")
    private Boolean authenticationEnabled;
    
    /** The username. */
    @Value("${app.trellis.authentication.username}")
    private String username;
   
    /** The password. */
    @Value("${app.trellis.authentication.password}")
    private String password;
    
    
    /** The uri factory endpoint. */
    @Value("${app.generator-uris.endpoint-link-uri}")
    private String uriFactoryEndpoint;

    // Constants
    private static final String TRELLIS = "trellis";
	private static final String STORAGE_NAME = "storageName";
	private static final String LOCAL_URI = "localURI";
	private static final String CANONICAL_LANGUAGE_URI = "canonicalLanguageURI";

    
    /** Rest Template. */
    @Autowired
    private RestTemplate restTemplate;

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
  
    /**
     * Exists container.
     *
     * @param message the message
     * @return true, if successful
     */
    @Override
    public boolean existsContainer(ManagementBusEvent message) {
        boolean result = false;
        
        String urlContainer =  trellisUrlEndPoint + "/" + message.getClassName();
        Model model;
        try {
            model = createRequestSpecification()
                    .header("Accept", MediaTypes.TEXT_TURTLE)
                    .expect()
                    .when().get(urlContainer)
                    .as(Model.class, new RdfObjectMapper(urlContainer));
                    result = model.size() > 0;
        } catch (Exception e) {
            result = false;
        }
        
        return result;  
    }

    /**
     * Creates the container.
     *
     * @param message the message
     */
    @Override
    public void createContainer(ManagementBusEvent message) {
        logger.info("Creating a container");
        
        Model model = ModelFactory.createDefaultModel();
        model.createProperty("http://hercules.org");
        Resource resourceProperties = model.createResource();
        Property a = model.createProperty("http://www.w3.org/ns/ldp#", "a");
        Property dcterms = model.createProperty("http://purl.org/dc/terms/", "title");
        
        resourceProperties.addProperty(a, "Container");
        resourceProperties.addProperty(a, "BasicContainer");
        resourceProperties.addProperty(dcterms, message.getClassName() + " Container");
        
        Response postResponse;
        try {
            postResponse = createRequestSpecification()
                    .contentType(MediaTypes.TEXT_TURTLE)
                    .header("slug", message.getClassName())                 
                    .header("link", "<http://www.w3.org/ns/ldp#BasicContainer>; rel=\"type\"")
                    .body(model, new RdfObjectMapper())
                    .post(trellisUrlEndPoint);
            
            if (postResponse.getStatusCode() != HttpStatus.SC_CREATED) {
                logger.warn("The container already exists: " + postResponse.getStatusCode());
            } else {
                logger.info("GRAYLOG-TS Creado contenedor de tipo: " + message.getClassName());
            }
        } catch (Exception e) {
            logger.error(e.getMessage());
            e.printStackTrace();
        }
        
    }

    /**
     * Creates the entry.
     *
     * @param message the message
     */
    @Override
    public void createEntry(ManagementBusEvent message) {
        Model model = trellisUtils.toObject(message.getModel());
        String urlContainer =  trellisUrlEndPoint + "/" + message.getClassName();
        
        // we only retrieve the id 
        String id = message.getIdModel().split("/")[message.getIdModel().split("/").length - 1];
        String factoryUriNotification = urlContainer + "/" + id;
        
        // we call to uri factory to notify the insertion
        logger.info("FactoryUriNotification: canonicalUri {}, localUri {}", message.getIdModel(), factoryUriNotification);
        this.eventNotifyUrisFactory(message.getIdModel(), factoryUriNotification);
        
        
        Response postResponse = createRequestSpecification()
                .contentType(MediaTypes.TEXT_TURTLE)
                .header("slug", id)
                .body(model, new RdfObjectMapper()).post(urlContainer);
        
        if (postResponse.getStatusCode() != HttpStatus.SC_CREATED) {
            logger.warn("Warn: saving the object: " + message.getModel());
            logger.warn("Operation: " + message.getOperation());
            logger.warn("cause: " + postResponse.getBody().asString());
            logger.warn("Warn: saving in Trellis the object: " + message.getModel());

        } else {
            logger.info("GRAYLOG-TS Creado recurso en trellis de tipo: " + message.getClassName());
        }
        
    }

    /**
     * Update entry.
     *
     * @param message the message
     */
    @Override
    public void updateEntry(ManagementBusEvent message) {
        String resourceID = trellisUtils.toResourceId(message.getIdModel());
        String urlContainer =  trellisUrlEndPoint.concat("/").concat(message.getClassName()).concat("/").concat(resourceID);
        
        Model model = trellisUtils.toObject(message.getModel());        
        Response postResponse = createRequestSpecification()
                .contentType(MediaTypes.TEXT_TURTLE)
                .body(model, new RdfObjectMapper()).put(urlContainer);
        
        if (postResponse.getStatusCode() != HttpStatus.SC_OK && postResponse.getStatusCode() != HttpStatus.SC_NO_CONTENT) {
            logger.error("Error updating the object: " + message.getModel());
            logger.error("Operation: " + message.getOperation());
            logger.error("cause: " + postResponse.getBody().asString());
            throw new RuntimeTrellisException("Error updating in Trellis the object: " + message.getModel());
        } else {
            logger.info("GRAYLOG-TS Actualizado recurso en trellis de tipo: " + message.getClassName());
        }        
    }

    /**
     * Delete entry.
     *
     * @param message the message
     */
    @Override
    public void deleteEntry(ManagementBusEvent message) {
        String resourceID = trellisUtils.toResourceId(message.getIdModel());
        String urlContainer =  trellisUrlEndPoint.concat("/").concat(message.getClassName()).concat("/").concat(resourceID);
        
        Response deleteResponse = createRequestSpecification().delete(urlContainer);
       
        if (deleteResponse.getStatusCode() != HttpStatus.SC_OK && deleteResponse.getStatusCode() != HttpStatus.SC_NO_CONTENT) {
            logger.error("Error deleting the object: {} - {}", message.getClassName(), message.getIdModel());
            logger.error("Operation: " + message.getOperation());
            logger.error("cause: " + deleteResponse.getBody().asString());
            throw new RuntimeTrellisException("Error deleting in Trellis the object: " + message.getClassName() + " - " + message.getIdModel());
        } else {
            logger.info("GRAYLOG-TS Eliminado recurso en trellis de tipo: " + message.getClassName());
        }        
    }

    /**
     * Creates the request specification and adds authentication if is required.
     *
     * @return the request specification
     */
    private RequestSpecification createRequestSpecification() {
        RequestSpecification requestSpecification = RestAssured.given();
        if(authenticationEnabled) {
            requestSpecification.header("Authorization", "Basic " + Base64.getEncoder().encodeToString((username + ":" + password).getBytes()));
        }
        return requestSpecification;
    }
    
    
    /**
     * Event notify uris factory.
     *
     * @param canonicalUri the canonical uri
     * @param localUri the local uri
     */
    private void eventNotifyUrisFactory(String cannonicalLanguageURI, String localURI) {
    	UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl(uriFactoryEndpoint)
    			.queryParam(TrellisOperationsImpl.CANONICAL_LANGUAGE_URI, cannonicalLanguageURI)
    			.queryParam(TrellisOperationsImpl.LOCAL_URI, localURI)
    			.queryParam(TrellisOperationsImpl.STORAGE_NAME, TrellisOperationsImpl.TRELLIS)
    			;
    	
    	Map<String, String> obj = new HashMap<String, String>();
    	obj.put(TrellisOperationsImpl.CANONICAL_LANGUAGE_URI, cannonicalLanguageURI);
    	obj.put(TrellisOperationsImpl.LOCAL_URI, localURI);
    	obj.put(TrellisOperationsImpl.STORAGE_NAME, TrellisOperationsImpl.TRELLIS);
		
		restTemplate.postForObject(builder.toUriString(), obj, Object.class);
    }

   
}