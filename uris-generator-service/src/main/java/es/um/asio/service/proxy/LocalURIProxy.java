package es.um.asio.service.proxy;

import com.izertis.abstractions.service.DeleteService;
import com.izertis.abstractions.service.QueryService;
import com.izertis.abstractions.service.SaveService;
import es.um.asio.service.filter.LocalURIFilter;
import es.um.asio.service.model.LocalURI;

import java.util.List;


/**
 * Proxy service for {@link LocalURI}. Performs DTO conversion and permission checks.
 */
public interface LocalURIProxy
        extends QueryService<LocalURI, String, LocalURIFilter>, SaveService<LocalURI>, DeleteService<LocalURI, String> {

    List<LocalURI> getAllByLocalURI(final LocalURI localURI);

    LocalURI getAllByLocalURIStr(final String localURI);

    LocalURI getAllByCanonicalURILanguageStrAndStorageTypeStr(final String canonicalURILanguage,final String storageTypeStr );
}