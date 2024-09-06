pub mod HTTP {
    use reqwest::{Response, Error};
    use std::collections::HashMap;
    use serde::Serialize;

    static BASE_URL: &str = "https://discord.com/api/";

    async fn get<K, V>(token: &str, endpoint: &str, parameters: &HashMap<K, V>) -> Result<Response, Error> {
        let client = reqwest::Client::new();
    
        let response = client
            .get(BASE_URL.to_owned() + endpoint)
            .header("Authorization", format!("Bot {}", token))
            
            .send()
            .await?;
        
        Ok(response)
    }
    
    async fn post<K, V>(token: &str, endpoint: &str, parameters: &HashMap<K, V>) -> Result<Response, Error> where K: Serialize, V: Serialize {
        let client = reqwest::Client::new();
    
        let response = client
            .post(BASE_URL.to_owned() + endpoint)
            .header("Authorization", format!("Bot {}", token))
            .header("Content-Type", "application/json")
            .body(serde_json::to_string(&parameters).unwrap())
            .send()
            .await?;
        
        Ok(response)
    }

    async fn patch<K, V>(token: &str, endpoint: &str, parameters: &HashMap<K, V>) -> Result<Response, Error> where K: Serialize, V: Serialize {
        let client = reqwest::Client::new();
    
        let response = client
            .patch(BASE_URL.to_owned() + endpoint)
            .header("Authorization", format!("Bot {}", token))
            .header("Content-Type", "application/json")
            .body(serde_json::to_string(&parameters).unwrap())
            .send()
            .await?;
        
        Ok(response)
    }
}