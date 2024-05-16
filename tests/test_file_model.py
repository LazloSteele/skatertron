from Skatertron.database import Base, session_manager, get_db_session
from Skatertron.models import File
from sqlalchemy.exc import IntegrityError


class TestFile:
    def setup_class(self):
        Base.metadata.create_all(session_manager.engine)

        self.session = get_db_session().__next__()

        self.valid_file = File(
            skate_id=1,
            file_name="109231093.mp4"
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_file_valid(self):
        self.session.add(self.valid_file)
        self.session.commit()

        buhbula_fs_video_1 = self.session.query(File).filter_by(
            file_name="109231093.mp4").first()

        assert buhbula_fs_video_1.skate_id == 1
        assert buhbula_fs_video_1.file_name != "Enver Invitational"

    def test_file_delete(self):
        test_file = self.session.query(File).filter_by(
            id=self.valid_file.id).first()
        test_id = test_file.id

        self.session.delete(test_file)
        self.session.commit()

        try:
            self.session.query(File).filter_by(
                id=test_id).first()
        except IntegrityError:
            self.session.rollback()
