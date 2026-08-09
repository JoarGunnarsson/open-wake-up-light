

async function doRequest(url, method, body){
    response = await fetch(url, {
        method: method,
        body: JSON.stringify(body),
    });

    if (!response.ok){
        throw new Error(`Response status code: ${response.status}`);
    }

    const result = await response.json();
    return result;
}

async function GET(url){
    response = await fetch(url, {
        method: "GET",
    });

    if (!response.ok){
        throw new Error(`Response status code: ${response.status}`);
    }

    const result = await response.json();
    return result;
}

async function POST(url, body=null){
    return doRequest(url, "POST", body)
}

async function PUT(url, body=null){
    return doRequest(url, "PUT", body)
}

async function DELETE(url){
    return doRequest(url, "GET", null)
}