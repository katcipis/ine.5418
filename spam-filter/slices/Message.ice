
module Messages {

    struct Msg {
        string domain;
        string subject;
        string body;
    };


    sequence<Msg> BlackListedMsgs;

    interface Client {
        
        void receiveMessage(Msg m);
        
        void receiveSpamBlacklist(BlackListedMsgs b);
    };


    interface Server {

       void setAsSpam(Msg m);

       void register(Client * c);
    };

};

