#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include "mailbox.hpp"

TEST_CASE("Mailbox teste 01 - send message")
{
    Database database("database.db");
    Mailbox mailbox(database);
    std::string message = "Oi!";
    std::string usernameReceiver = "MarceloM";
    int sent = mailbox.sendMessage(message, 35, usernameReceiver);
    CHECK(sent == 0);
}


TEST_CASE("Mailbox teste 02 - see chat")
{
    Database database("database.db");
    Mailbox mailbox(database);
    std::string usernameReceiver = "MarceloM";
    std::vector <std::string> chat = mailbox.readMessages(35, usernameReceiver);
    CHECK(!chat.empty());
}

TEST_CASE("Mailbox teste 03 - cannot see chat")
{
    Database database("database.db");
    Mailbox mailbox(database);
    std::string usernameReceiver = "Gloria(ModernFamily)";
    CHECK_THROWS_AS(mailbox.readMessages(35, usernameReceiver), NotFriend);
}

