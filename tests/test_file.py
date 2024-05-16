from Skatertron.database import Base, session_manager, get_db_session
from Skatertron.models import File


class TestFile:
    def setup_class(self):
        Base.metadata.create_all(session_manager.engine)

        self.session = get_db_session().__next__()

        self.valid_file = File(
            skate_id=8,
            file_name="109231093.mp4"
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_event_valid(self):
        self.session.add(self.valid_file)
        self.session.commit()

        buhbula_fs_video_1 = self.session.query(File).filter_by(
            file_name="109231093.mp4").first()

        assert buhbula_fs_video_1.skate_id == 8
        assert buhbula_fs_video_1.file_name != "Enver Invitational"
