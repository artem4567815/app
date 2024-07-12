import SwiftUI

struct ContentView: View
{
    @State var games = [Game]()
    @State private var searchText = ""
    @State var lastDate: Double = 0

    var body: some View {
        
        NavigationView {
            //$0.title.contains(searchText)
            //.filter({searchText.isEmpty ? true : true})
            List(games) { game in
                //GamePage(gamename: game.title)
                NavigationLink {
                    GamePage(gamename: game.name)
                } label: {
                    HStack(spacing: 30) {
                        if #available(iOS 15.0, *) {
                            AsyncImage(url: URL(string: game.img)!) {
                                image in
                                image
                                    .resizable()
                                    .scaledToFill()
                            } placeholder: {
                                Color.gray.opacity(0.3)
                            }
                            .frame(width: 100, height: 55)
                        } else {
                            Text("НЕ РАБОТАЕТ БЛЯТЬ!!!!")
                        }
                        
                        VStack(alignment: .leading) {
                            Text("\(game.name)").bold().lineLimit(1)
                            Text("Цена Steam: \(game.price ?? "Не найдено")")
                            Text("Цена Epic: \(game.epic_price ?? "Не найдено")").foregroundColor(.red)
                        }
                    }
                }
            }
            .onChange(of: searchText, {
                var curDate = Date.now.timeIntervalSince1970 * 1000.0
                if(curDate - lastDate >= 1000) {
                    Api().loadData(url: "http://localhost:5000/search/\(searchText)") { games in
                        self.games = games
                    }
                    lastDate = Date.now.timeIntervalSince1970 * 1000.0
                }
            })
            .searchable(text: $searchText, prompt: "Например: Fallout 4")
            .listRowSeparator(.automatic, edges: .all)
        }
    }
    
}


struct GamePage: View {
    
    let name: String
    @StateObject var model: GamePageClass
    
    init(gamename: String) {
        name = gamename
        
        self._model = .init(wrappedValue: GamePageClass(gamename: gamename))
    }
    
    
    var body: some View {
        VStack {
            AsyncImage(url: URL(string: model.gameInfo.img)!) {
                image in
                image
                    .resizable()
                    .scaledToFill()
            } placeholder: {
                Color.gray.opacity(0.3)
            }
            .frame(width: 400, height: 200)
            
            Text("\(name)")
            Text("Описание: \(model.gameInfo.description ?? "Не найдено")")
            Text("Рейтинг: \(model.gameInfo.review == nil ? "Не найдено" : "\(Int(model.gameInfo.review!)) \\ 100")")
            Text("Время прохождения: \(model.gameInfo.playtime ?? "Не найдено")")
            Text("Цена: \(model.gameDetails.current_price ?? "Не найдено")")
            Text("Цена без скидки: \(model.gameDetails.initial_price ?? "Не найдено")")
            Text("Скидка: \(model.gameDetails.discount  == nil ? "Не найдено" : "\(model.gameDetails.discount!)%")")
        }
        .task {
            model.loadGameInfo(url: "http://localhost:5000/details/\(name)")
            model.loadGameDetails(url: "http://localhost:5000/prices/\(name)/Russia")
        }
         
    }
}

class GamePageClass: ObservableObject {
    
    var name: String = ""
    
    init(gamename: String) {
        print(gamename)
        name = gamename
    
        //loadGameInfo(url: "http://localhoast:5000/gameInfo")
        print("GET DETAILS")
        //loadGameInfo(url: "http://localhost:5000/details/\(name)")
        print("GET DETAILS DONE")
    }
    
    @Published var gameInfo: GameInfo = GameInfo(img: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQd7S5iS77v4PL22VL4m7St-gcwzcg7o1DE2Q&s")
    @Published var gameDetails: GameDetails = GameDetails(current_price: "", initial_price: "", discount: 0, currency: "")
    
    func loadGameInfo(url: String) {
        print("load info 1")
        guard var url = URL(string: url) else {
            print("The url was invalid!")
            return
        }
        
        print("load info 2")
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        
        print("load info 3")
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error as? NSError {
                print("1111----\(error)")
            }
            if(data == nil) {
                self.gameInfo = GameInfo(img: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQd7S5iS77v4PL22VL4m7St-gcwzcg7o1DE2Q&s")
                print("NO DATA Load Info!!!!")
                return
            }
            print("DATA Load Info!!!!")
            let gameInfoParce = try! JSONDecoder().decode(GameInfo.self, from: data!)
            DispatchQueue.main.async { [weak self] in
                self?.gameInfo = gameInfoParce
            }
            
        }.resume()
        
        print("load info 4")
        
        
        
    }
    
    
    func loadGameDetails(url: String) {
        print("url in country request: \(url)")
        guard let url = URL(string: url) else {
            print("The url was invalid!")
            return
        }
        
        print("load info 6")
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        
        print("load info 7")
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error as? NSError {
                print("1111----\(error)")
            }
            if(data == nil) {
                self.gameInfo = GameInfo(img: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQd7S5iS77v4PL22VL4m7St-gcwzcg7o1DE2Q&s")
                print("NO DATA Load Info!!!!")
                return
            }
            print("Data: \(response)")
            let gameDetailsParce = try! JSONDecoder().decode(GameDetails.self, from: data!)
            DispatchQueue.main.async { [weak self] in
                self?.gameDetails = gameDetailsParce
            }
            
        }.resume()
        
        print("load info 8")
    }
     
}


#Preview {
    ContentView()
}
