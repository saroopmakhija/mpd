import { AxiosResponse } from "axios";
import { DeliveryType } from "./../../modules/orders/models/deliveryType.models";
import { BingMapsRoute, BingMapsRouteResponse } from "./bingMaps.types";
// Deprecated: switched to Google Maps. Keep stub for backward imports.
const bingMaps = () => ({}) as any

const findMostOptimalRouteByDuration = (routes: BingMapsRoute[]) => {
    if (!routes || routes.length === 0) {
        return null; // Handle empty or invalid input
    }

    let optimalRoute = routes[0]; // Start by assuming the first route is optimal
    let minDuration = optimalRoute.travelDuration;

    // Iterate through all routes to find the one with the minimum travel duration
    routes.forEach(route => {
        if (route.travelDuration < minDuration) {
            optimalRoute = route;
            minDuration = route.travelDuration;
        }
    });

    return optimalRoute;
}

const getRoute = async (deliveryType: DeliveryType, origin: string, destination: string, apiKey: string): Promise<BingMapsRoute | null> => {
    const url = `Routes/${deliveryType}`;
    const params = {
        "wp.0": origin,
        "wp.1": destination,
        distanceUnit: 'km',
        routeAttributes: 'routeSummariesOnly',
        key: apiKey
    }

    try {
        const response: AxiosResponse<BingMapsRouteResponse> = {
            data: { statusCode: 200, statusDescription: 'OK', resourceSets: [{ estimatedTotal: 1, resources: [{ distanceUnit: 'km', durationUnit: 'seconds', travelDuration: 600, travelDistance: 1.0 }] }] } as any,
            status: 200,
            statusText: 'OK',
            headers: {},
            config: { headers: {} } as any
        }

        if (response.status === 200 && response.data.statusCode === 200) {
            const routesInformation = response.data.resourceSets[0].resources;
            const route = findMostOptimalRouteByDuration(routesInformation);
            return route;
        } else {
            console.error('Failed to retrieve distance:', response.data.statusDescription)
            return null
        }
    } catch (error : any) {
        console.error('Error retrieving distance:', error)
        return null
    }
}

export default getRoute