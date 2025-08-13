import axios, { AxiosResponse } from "axios";
import { DeliveryType } from "../../modules/orders/models/deliveryType.models";
import { GoogleMapsDistanceMatrixResponse, GoogleMapsRoute } from "./googleMaps.types";

const getRoute = async (deliveryType: DeliveryType, origin: string, destination: string, apiKey: string): Promise<GoogleMapsRoute | null> => {
    const url = 'https://maps.googleapis.com/maps/api/distancematrix/json';

    // Map delivery type to Google Maps travel mode
    const travelMode = deliveryType === DeliveryType.WALKING ? 'walking' : 'driving';

    const params = {
        origins: origin,
        destinations: destination,
        mode: travelMode,
        units: 'metric',
        key: apiKey,
        // Optimize for Indian traffic conditions
        region: 'in',
        language: 'en'
    };

    try {
        const response: AxiosResponse<GoogleMapsDistanceMatrixResponse> = await axios.get(url, { params });
        const data = response.data;

        if (data.status === 'OK' && data.rows && data.rows.length > 0) {
            const element = data.rows[0].elements[0];
            
            if (element.status === 'OK') {
                return {
                    distance: element.distance.value / 1000, // Convert meters to kilometers
                    duration: element.duration.value, // Already in seconds
                    distanceText: element.distance.text,
                    durationText: element.duration.text
                };
            } else {
                console.warn(`Google Maps route calculation failed: ${element.status}`);
                return null;
            }
        } else {
            console.warn(`Google Maps Distance Matrix API failed: ${data.status}`);
            return null;
        }
    } catch (error) {
        console.error('Error calculating route with Google Maps:', error);
        return null;
    }
};

export default getRoute;


