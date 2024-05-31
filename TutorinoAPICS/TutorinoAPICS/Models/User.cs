namespace TutorinoAPICS.Models
{
    public class User
    {
        public int Id { get; set; }
        public String UserName { get; set; }
        public String UserSurname { get; set; }
    }

    public class UserAdded
    {
        public String UserName { get; set; }
        public String UserSurname { get; set; }
        public String UserLogin { get; set; }
        public String UserEmail { get; set; }
        public String UserPassword { get; set; }
        public String AccountType {get; set;}
    }

    public class UserLogin
    {
        public String Username { get; set; }
        public String Email { get; set; }
        public String Password { get; set; }
    }

    public class UserFunction
    {
        public int userID {get; set;}
        public String AccountType {get;set;}
    }
}
