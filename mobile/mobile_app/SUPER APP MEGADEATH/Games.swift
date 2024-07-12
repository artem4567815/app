//
//  Games.swift
//  SUPER APP MEGADEATH
//
//  Created by Student on 10.07.2024.
//

import Foundation
import SwiftUI
struct Game: Codable, Identifiable
{
    let id = UUID()

    var name: String
    var epic_price: String?
    var price: String?
    var img: String
    
}

class Api: ObservableObject {
    @Published var games = [Game]()
    func loadData(url: String, completion: @escaping ([Game]) -> ()) {
        guard let url = URL(string: url) else {
            print("The url was invalid!")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
            
        URLSession.shared.dataTask(with: request) { data, response, error in
            print(data ?? "NO DATA Load Data!!!!")
            let games = try! JSONDecoder().decode([Game].self, from: data!)
            
            DispatchQueue.main.async {
                completion(games)
            }
        }.resume()
    }
}

struct GameInfo: Codable
{
    var img: String
    var description: String?
    var review: Float?
    var playtime: String?
}

struct GameDetails: Codable, Identifiable
{
    let id = UUID()
    var current_price: String?
    var initial_price: String?
    var discount: Int?
    var currency: String?
}

