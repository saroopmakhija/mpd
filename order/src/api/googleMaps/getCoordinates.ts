import axios, { AxiosResponse } from "axios";
import { GoogleMapsGeocodingResponse, Coordinates } from "./googleMaps.types";

const getCoordinates = async (address: string, apiKey: string): Promise<Coordinates | null> => {
    const url = 'https://maps.googleapis.com/maps/api/geocoding/json';

    const params = {
        address: address,
        key: apiKey,
        // Bias towards Indian addresses
        region: 'in',
        language: 'en'
    };

    try {
        const response: AxiosResponse<GoogleMapsGeocodingResponse> = await axios.get(url, { params });
        const data = response.data;

        if (data.status === 'OK' && data.results && data.results.length > 0) {
            const location = data.results[0].geometry.location;
            return {
                latitude: location.lat,
                longitude: location.lng
            };
        } else {
            console.warn(`Google Maps Geocoding failed: ${data.status}`);
            return null;
        }
    } catch (error) {
        console.error('Error fetching coordinates from Google Maps:', error);
        return null;
    }
};

export default getCoordinates;


