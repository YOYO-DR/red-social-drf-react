import axios from "axios";
import createAuthRefreshInterceptor from "axios-auth-refresh";
import { getAccessToken, getRefreshToken } from "../hooks/user.actions";

const axiosService = axios.create({ // creo una instancia de axios
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

axiosService.interceptors.request.use(async (config) => { // esto es un interceptor, en este caso es para los request, se ejecuta antes de que se haga la solicitud
  /**
  * Recuperar el token de acceso de localStorage y agregarlo a los encabezados de
la solicitud
  */
  
  config.headers.Authorization = `Bearer ${getAccessToken()}`;
  return config;
});

// Interceptor para manejar errores de respuesta, aunque esto es algo que ya se hace por defecto en axios, pero se puede personalizar
axiosService.interceptors.response.use(
  (res) => Promise.resolve(res),
  (err) => Promise.reject(err)
);

// esta funcion se ejecutara cuando el token de acceso haya expirado, osea que reciba un codigo de estado 401 - no autorizado
const refreshAuthLogic = async (failedRequest) => {
  // el failedRequest es la solicitud que fallo, en este caso es la solicitud que fallo por el token de acceso

  return axios
    .post("/refresh/token/", null, { // se hace una solicitud para obtener un nuevo token de acceso, como se observa, no se ejcuta con axiosService, sino con axios, ya que axiosService tiene un interceptor que se ejecuta antes de hacer la solicitud, y en este caso no se quiere que se ejecute
      baseURL: "http://localhost:8000",
      headers: {
        Authorization: `Bearer ${getRefreshToken()}`,
      },
    })
    .then((resp) => {
      const { access, refresh, user } = resp.data; // se obtiene el nuevo token de acceso y el nuevo token de actualizacion

      failedRequest.response.config.headers["Authorization"] =
        "Bearer " + access; // se agrega el nuevo token de acceso a los encabezados de la solicitud que fallo, el cual se ejecutara de nuevo
      
      localStorage.setItem( // y tambien se guarda en el localStorage
        "auth",
        JSON.stringify({
          access,
          refresh,
          user
        })
      );
    })
    .catch(() => { // si falla la solicitud para obtener un nuevo token de acceso, se elimina el token de acceso y el token de actualizacion del localStorage
      localStorage.removeItem("auth");
    });
};


// se crea un interceptor para manejar la actualizacion del token de acceso, cada que se ejecute una solicitud y se reciba un codigo de estado 401 - no autorizado, se ejecutara la funcion refreshAuthLogic
createAuthRefreshInterceptor(axiosService, refreshAuthLogic);

export function fetcher(url) { // funcion para las peticiones get, se ejecuta con axiosService
  return axiosService.get(url).then((res) => res.data);
}
export default axiosService;
