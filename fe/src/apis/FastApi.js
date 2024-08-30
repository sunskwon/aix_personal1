const baseUrl = "http://localhost:8000";

export async function GetAPI(address) {

    const url = baseUrl + address;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Access-Cross-Allow-Origin': '*',
            },
        });

        return response;
    } catch (error) {
        console.error(error);
    };
};

export async function PostAPI(address, Object) {

    const url = baseUrl + address;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Access-Cross-Allow-Origin': '*',
            },
            body: JSON.stringify(Object),
        });

        return response;
    } catch (error) {
        console.error(error);
    };
};