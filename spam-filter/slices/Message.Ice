
module Messages {

    struct Msg {
        string domain;
        string subject;
        string body;
    };


    interface Client {
        
        void receiveMessage(Msg message);
        
        void receiveSpamBlacklist(sequence<Msg> blacklist);
    };


    interface Server {

       void setAsSpam(Msg message);

       void register(Client * client);
    };

};

