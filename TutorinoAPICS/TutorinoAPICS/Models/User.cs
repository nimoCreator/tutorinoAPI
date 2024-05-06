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
    }
}
