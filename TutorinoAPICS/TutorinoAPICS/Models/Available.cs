namespace TutorinoAPICS.Models
{
    public class Available
    {
        public int user_uuid {get;set;}
        public int weekday {get;set;}
        public int begin {get;set;}
        public int end {get;set;}
        public DateTime valid_from {get;set;}
        public DateTime valid_until {get;set;}
    }

    public class AvailableChange
    {
        public int aid {get;set;}
        public int user_uuid {get;set;}
    }

    public class AvalID
    {
        public int user_uuid { get; set; }
    }

    public class AvailableFull
    {
        public int aid { get;set;}
        public int user_uuid { get; set; }
        public int weekday { get; set; }
        public int begin { get; set; }
        public int end { get; set; }
        public DateTime valid_from { get; set; }
        public DateTime valid_until { get; set; }
    }
}
