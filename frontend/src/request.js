

async function doRequest(url, method, body){
    let request = {
        method: method,
        headers: {
            "Content-Type": "application/json",
        },
    };
    if (body != null){
        request.body = JSON.stringify(body);
    }
    let response = await fetch(url, request);

    if (!response.ok){
        throw new Error(`Response status code: ${response.status}`);
    }

    const result = await response.json();
    return result;
}

export async function GET(url){
    return doRequest(url, "GET", null)
}

export async function POST(url, body=null){
    return doRequest(url, "POST", body)
}

export async function PUT(url, body=null){
    return doRequest(url, "PUT", body)
}

export async function DELETE(url){
    return doRequest(url, "DELETE", null)
}


